import pygame
from pygame import Surface

from typing import Optional, Type

from .config import Config
from .constants import Constants
from .handlers import GameEventHandler, GameEventType, CustomClassHandler, AnimationHandler
from .renderables import Screen


class Game:
    """
    Entry point for your game.
    Requires a pygame display Surface to be passed into the constructor,
    and .screen to be set to a valid Screen object, before calling .start() to begin the game loop
    """

    def __init__(self, window: Surface, config=Config):
        pygame.mixer.pre_init(frequency=Constants.AUDIO_FREQUENCY)
        pygame.init()
        pygame.mixer.init()

        self._window = window
        self._config = config

        # These attributes are not yet initialised. They are initialised when their respective properties are first set
        self._tick_rate = None
        self._tick_delay_ms = None
        self._fps = None
        self._frame_delay_ms = None
        self._max_frame_delay_ms = None
        self._screen = None

        # Initialising some of the above attributes
        self.tick_rate = config.TICK_RATE
        self.fps = config.FPS

        self._ms_since_update = 0
        self._ms_since_render = 0
        self._tick_number = 0  # Counts up by 1 per update until it reaches the game's tick rate, then resets to 0
        self._clock = pygame.time.Clock()

        # Game-level handlers
        self._game_event_handler = GameEventHandler()
        self._custom_class_handler = CustomClassHandler(self)
        self._animation_handler = AnimationHandler(self)

    @property
    def window(self) -> Surface:
        return self._window

    @property
    def config(self) -> Type[Config]:
        return self._config

    @property
    def tick_rate(self) -> float:
        return self._tick_rate

    @tick_rate.setter
    def tick_rate(self, value: float):
        self._tick_rate = value
        self._tick_delay_ms = 0 if value == 0 else (1000/value)

    @property
    def fps(self) -> float:
        return self._fps

    @fps.setter
    def fps(self, value: float):
        self._fps = value
        self._frame_delay_ms = 0 if value == 0 else (1000/value)
        self._max_frame_delay_ms = max(self._frame_delay_ms, 1000)

    @property
    def screen(self) -> Optional[Screen]:
        return self._screen

    @screen.setter
    def screen(self, value: Screen):
        if value is self._screen:
            return

        with self._game_event_handler(GameEventType.CHANGE_SCREEN, self._screen, value):
            self._screen = value

    @property
    def game_event_handler(self) -> GameEventHandler:
        return self._game_event_handler

    @property
    def custom_class_handler(self) -> CustomClassHandler:
        return self._custom_class_handler

    @property
    def animation_handler(self) -> AnimationHandler:
        return self._animation_handler

    def start(self) -> None:
        if self._screen is None:
            raise RuntimeError("a valid Screen object must be set to .screen before the game can be started")

        while True:
            # Update the game state
            self._add_elapsed()
            current_tick_delay_ms = self._tick_delay_ms  # Current tick delay copied in case it's altered during update
            while self._ms_since_update >= current_tick_delay_ms:
                """
                This inner loop allows for multiple updates before a fresh render, if the actual tick rate is
                sufficiently behind the expected tick rate to require it.

                This 'catching up' is necessary to ensure tick rate is as consistent as possible when the game is
                experiencing performance issues, thus ensuring that game *behaviour* in turn is as consistent as
                possible in a given amount of real time, regardless of frame rate
                """

                if current_tick_delay_ms == 0:
                    self._update_screen(self._ms_since_update)
                    self._ms_since_update = 0
                    break
                else:
                    self._update_screen(current_tick_delay_ms)
                    self._ms_since_update -= current_tick_delay_ms

            # Render to the display
            self._add_elapsed()
            if self._ms_since_render >= self._frame_delay_ms:
                self._render_screen()
                self._ms_since_render -= self._frame_delay_ms

                """
                The frame rate will only keep track of how far behind it is up to one frame or one second behind,
                whichever is larger.

                This is a choice made for the sake of performance - if the framerate falls heavily behind, it is
                not important to render many frames in a row in order to catch up; once a new frame has been rendered,
                at that point in time the display is now showing the most up to date view possible and so does not need
                to catch up further for the player's sake. Therefore, tracking *any* delay at all is only done
                for the sake of attempting to match the expected frame rate (assuming the game is coping
                sufficiently well for this not to be a performance problem)
                """
                self._ms_since_render = min(self._ms_since_render, self._max_frame_delay_ms)

    def _add_elapsed(self) -> None:
        elapsed_ms = self._clock.tick()
        self._ms_since_update += elapsed_ms
        self._ms_since_render += elapsed_ms

    def _update_screen(self, elapsed_ms: int) -> None:
        input_events = list(self.config.GET_INPUT_EVENTS())  # Repackaged into a list to be consumed from it as needed

        with self.game_event_handler(GameEventType.UPDATE, self._tick_number, elapsed_ms, input_events):
            self._screen.update(self._tick_number, elapsed_ms, input_events)

        self._tick_number += 1
        if self._tick_number >= self._tick_rate:
            self._tick_number = 0

    def _render_screen(self) -> None:
        updated_rects = self._screen.render(self._window)

        with self._game_event_handler(GameEventType.RENDER, updated_rects):
            pygame.display.update(updated_rects)

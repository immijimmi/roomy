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

        self._tick_rate = None
        self._fps = None
        self._tick_delay_ms = None
        self._frame_delay_ms = None

        self.tick_rate = config.TICK_RATE
        self.fps = config.FPS

        self._ms_since_update = 0
        self._ms_since_render = 0
        self._clock = pygame.time.Clock()
        self._screen = None

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
            elapsed_ms = self._clock.tick()
            self._ms_since_update += elapsed_ms
            self._ms_since_render += elapsed_ms

            current_tick_delay_ms = self._tick_delay_ms  # Current tick delay copied incase it's altered during update
            while self._ms_since_update >= current_tick_delay_ms:
                if current_tick_delay_ms == 0:
                    self._update_screen(self._ms_since_update)
                    self._ms_since_update = 0
                    break
                else:
                    """
                    Rather than setting `._ms_since_update` to 0 below after a single update, instead the expected
                    tick delay is removed from it each time an update is completed until the remaining value is less
                    than the expected tick delay.

                    This differs from how `._ms_since_render` is handled, because for game ticks the actual tick rate
                    needs to hold as strictly as possible to the expected tick rate to ensure that game behaviour is
                    always as consistent as possible in any given amount of real time.

                    The difference in behaviour that results from this is that when game ticks fall behind, they will
                    not 'reset' after a late tick but will instead complete multiple updates in a row if necessary before
                    a new render is completed in order to catch up to the expected tick rate.

                    In contrast, when *renders* fall behind they *will* 'reset' after a late render, because as of the
                    latest rendered frame the game is now displaying a completely up-to-date view of the game state
                    """

                    self._update_screen(current_tick_delay_ms)
                    self._ms_since_update -= current_tick_delay_ms

            if self._ms_since_render >= self._frame_delay_ms:
                self._render_screen()
                self._ms_since_render = 0

    def _update_screen(self, elapsed_ms: int) -> None:
        input_events = list(self.config.GET_INPUT_EVENTS())  # Repackaged into a list to be consumed from it as needed

        with self.game_event_handler(GameEventType.UPDATE, elapsed_ms, input_events):
            self._screen.update(elapsed_ms, input_events)

    def _render_screen(self) -> None:
        updated_rects = self._screen.render(self._window)

        with self._game_event_handler(GameEventType.RENDER, updated_rects):
            pygame.display.update(updated_rects)

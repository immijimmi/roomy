import pygame
from pygame import Surface

from typing import Optional, Type

from .config import Config
from .constants import Constants
from .utils import GameEventHandler, GameEventType, ClassRegistrar, AnimationCache
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

        self._config = config
        self._window = window

        self._tick_rate = None
        self._tick_delay_ms = None
        self.tick_rate = config.TICK_RATE

        self._fps = None
        self._frame_delay_ms = None
        self.fps = config.FPS

        self._screen = None

        self._ms_since_tick = 0
        self._ms_since_frame = 0

        self._clock = pygame.time.Clock()

        # Game-level utilities
        self._game_event_handler = GameEventHandler()
        self._class_registrar = ClassRegistrar(self)
        self._animation_cache = AnimationCache(self)

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

        with self._game_event_handler(GameEventType.CHANGE_SCREEN, old_screen=self._screen, new_screen=value):
            self._screen = value

    @property
    def game_event_handler(self) -> GameEventHandler:
        return self._game_event_handler

    @property
    def class_registrar(self) -> ClassRegistrar:
        return self._class_registrar

    @property
    def animation_cache(self) -> AnimationCache:
        return self._animation_cache

    def start(self) -> None:
        if self._screen is None:
            raise RuntimeError("a valid Screen object must be set to .screen before the game can be started")

        self._clock.tick()  # Initial call to reset any accrued time between initialisation and running this method

        while True:
            # Copied in case it's altered during an update
            current_tick_delay_ms = self._tick_delay_ms
            # Copied in case it's altered during an update
            current_frame_delay_ms = self._frame_delay_ms

            # Carry out updates as needed

            if current_tick_delay_ms == 0:
                # Run only 1 tick per loop since there's no set tick rate
                self._tick(self._ms_since_tick)
                self._ms_since_tick = 0
            else:
                # Run as many ticks as needed to catch up
                while self._ms_since_tick >= current_tick_delay_ms:
                    self._tick(current_tick_delay_ms)
                    self._ms_since_tick -= current_tick_delay_ms

            # Run 1 frame, passing in the entire elapsed ms (only 1 frame is ever needed to catch up)
            self._frame(self._ms_since_tick, self._ms_since_frame)
            self._ms_since_frame = 0

            # Add elapsed time

            if (current_frame_delay_ms == 0) or (current_tick_delay_ms == 0):
                elapsed = self._clock.tick()
            else:
                ms_till_tick = current_tick_delay_ms - self._ms_since_tick
                ms_till_frame = current_frame_delay_ms - self._ms_since_frame

                elapsed = self._clock.tick(1000/min(ms_till_tick, ms_till_frame))

            self._ms_since_tick += elapsed
            self._ms_since_frame += elapsed

    def _tick(self, ms_since_last_tick: int) -> None:
        input_events = pygame.event.get()

        with self.game_event_handler(GameEventType.TICK, ms_since_last_tick=ms_since_last_tick):
            self._screen.tick(ms_since_last_tick, input_events)

    def _frame(self, ms_since_last_tick: int, ms_since_last_frame: int) -> None:
        with self._game_event_handler(
                GameEventType.FRAME,
                ms_since_last_tick=ms_since_last_tick, ms_since_last_frame=ms_since_last_frame
        ):
            self._screen.frame(ms_since_last_tick, ms_since_last_frame)

            updated_rects = self._screen.render(self._window)
            pygame.display.update(updated_rects)

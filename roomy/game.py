import pygame
from pygame import Surface

from typing import Optional, Type

from .config import Config
from .constants import Constants
from .handlers import GameEventHandler, GameEventKey, CustomClassHandler, AnimationHandler
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

        self.fps = config.FPS
        self.updates_per_frame = config.UPDATES_PER_FRAME

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
    def screen(self) -> Optional[Screen]:
        return self._screen

    @screen.setter
    def screen(self, value: Screen):
        if value is self._screen:
            return

        with self._game_event_handler(GameEventKey.CHANGE_SCREEN, self._screen, value):
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
            for update_index in range(self.updates_per_frame):
                self._update_screen()

            self._render_screen()

    def _update_screen(self) -> None:
        elapsed_ms = self._clock.tick(self.fps * self.updates_per_frame)
        input_events = list(self.config.GET_INPUT_EVENTS())  # Repackaged into a list to be consumed from it as needed

        self._screen.update(elapsed_ms, input_events)

    def _render_screen(self) -> None:
        updated_rects = self._screen.render(self._window)

        pygame.display.update(updated_rects)

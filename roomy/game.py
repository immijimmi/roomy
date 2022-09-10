import pygame
from pygame import Surface

from typing import Optional

from .config import Config
from .constants import Constants
from .handlers import EventHandler, CustomClassHandler, EventKey
from .renderables import Screen


class Game:
    """
    Entry point for your game.
    Requires a pygame display Surface to be passed into the constructor,
    and .screen to be set to a valid Screen object, before calling .start() to begin the game loop
    """

    def __init__(self, window: Surface, fps: int = 0, updates_per_frame: int = 1, config: Config = Config):
        pygame.mixer.pre_init(frequency=Constants.AUDIO_FREQUENCY)
        pygame.init()
        pygame.mixer.init()

        self._window = window
        self._config = config

        self.fps = fps
        self.updates_per_frame = updates_per_frame

        self._clock = pygame.time.Clock()
        self._screen = None

        # Game-level handlers
        self._event_handler = EventHandler()
        self._custom_class_handler = CustomClassHandler(self)

    @property
    def window(self) -> Surface:
        return self._window

    @property
    def config(self) -> Config:
        return self._config

    @property
    def screen(self) -> Optional[Screen]:
        return self._screen

    @screen.setter
    def screen(self, value: Screen):
        if value is self._screen:
            return

        with self._event_handler(EventKey.CHANGE_SCREEN, self._screen, value):
            self._screen = value

    @property
    def event_handler(self) -> EventHandler:
        return self._event_handler

    @property
    def custom_class_handler(self) -> CustomClassHandler:
        return self._custom_class_handler

    def start(self) -> None:
        if self._screen is None:
            raise RuntimeError("a valid Screen object must be set to .screen before the game can be started")

        while True:
            for update_index in range(self.updates_per_frame):
                self._update_screen()

            self._render_screen()

    def _update_screen(self) -> None:
        elapsed_ms = self._clock.tick(self.fps * self.updates_per_frame)
        events = list(pygame.event.get())  # Events are passed in a list so that they can be consumed if necessary

        self._screen.update(elapsed_ms, events)

    def _render_screen(self) -> None:
        updated_rects = self._screen.render(self._window)

        pygame.display.update(updated_rects)

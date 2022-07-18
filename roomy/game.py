import pygame
from pygame import Surface

from typing import Type

from .constants import Constants
from .handlers import ObserverHandler
from .screens import Screen


class Game:
    """
    Entry point for your game.
    Requires a pygame display Surface and a Screen object to be passed into the constructor,
    and then for .start() to be called to begin the game loop
    """

    def __init__(self, window: Surface, initial_screen: Screen, fps: int = 0):
        pygame.mixer.pre_init(frequency=Constants.AUDIO_FREQUENCY)
        pygame.init()
        pygame.mixer.init()

        self._window = window
        self._screen = initial_screen

        self.fps = fps
        self._clock = pygame.time.Clock()

        self._observer_handler = ObserverHandler

    @property
    def screen(self) -> Screen:
        return self._screen

    @screen.setter
    def screen(self, value: Screen):
        old_screen = self._screen
        self._screen = value

        self._observer_handler.on_change_screen(old_screen, value)

    @property
    def window(self):
        return self._window

    @property
    def observer_handler(self) -> Type[ObserverHandler]:
        return self._observer_handler

    def start(self) -> None:
        while True:
            self._update_screen()
            self._render_screen()

    def _update_screen(self) -> None:
        elapsed_ms = self._clock.tick(self.fps)
        events = list(pygame.event.get())  # Events are passed in a list so that they can be consumed if necessary

        self._screen.update(elapsed_ms, events)

    def _render_screen(self) -> None:
        updated_rects = self._screen.render(self._window)

        pygame.display.update(updated_rects)

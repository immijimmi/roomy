import pygame

from typing import Type, Sequence, Tuple

from .cls import *
from .constants import Constants


class Game:
    fps = 144

    def __init__(self, resolution: Sequence[int], initial_screen: Screen):
        self._resolution = (resolution[0], resolution[1])
        self._screen = initial_screen
        self._observer_manager = ObserverManager

        pygame.mixer.pre_init(frequency=Constants.AUDIO_FREQUENCY)
        pygame.init()
        pygame.mixer.init()

        self._window = pygame.display.set_mode(self._resolution)
        self._clock = pygame.time.Clock()

    @property
    def resolution(self) -> Tuple[int, int]:
        return self._resolution

    @property
    def screen(self) -> Screen:
        return self._screen

    @screen.setter
    def screen(self, value: Screen):
        old_screen = self._screen
        self._screen = value

        self._observer_manager.on_change_screen(old_screen, value)

    @property
    def observer_manager(self) -> Type[ObserverManager]:
        return self._observer_manager

    @property
    def window(self):
        return self._window

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

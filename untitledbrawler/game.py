from managedstate import State
from managedstate.extensions import Listeners, Registrar
import pygame

from json import loads

from .cls import *


class Game:
    resolution = (1280, 720)
    fps = 144

    def __init__(self):
        self._observers = ObserverManager(self)

        pygame.init()
        self._window = pygame.display.set_mode(self.resolution)
        self._clock = pygame.time.Clock()

        self._screen = None

        self._init_screen()
        self.run()

    @property
    def observers(self) -> ObserverManager:
        return self._observers

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def window(self):
        return self._window

    def change_screen(self, new_screen: Screen) -> None:
        old_screen = self._screen
        self._screen = new_screen

        self._observers.on_change_screen(old_screen, new_screen)

    def run(self) -> None:
        while True:
            self.update()
            self.render()

    def update(self) -> None:
        elapsed_ms = self._clock.tick(self.fps)
        events = tuple(pygame.event.get())

        self._screen.update(elapsed_ms, events)

    def render(self) -> None:
        updated_rects = self._screen.render(self._window)

        pygame.display.update(updated_rects)

    def _init_screen(self):
        state_extended_class = State.with_extensions(Registrar, Listeners)

        save_states = []
        for potential_save_filename in ("save1.json", "save2.json", "save3.json"):
            try:
                with open(potential_save_filename, "r") as file:
                    save_state = state_extended_class(loads(file.read()))
            except FileNotFoundError:
                save_state = state_extended_class()

            save_states.append(save_state)

        ##### TODO: Replace with logic to load menu screen once it is designed
        self.change_screen(World(self, save_states[0]))

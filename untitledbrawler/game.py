from managedstate import State
from managedstate.extensions import Listeners, Registrar
import pygame

from json import loads

from .cls import *


class Game:
    resolution = (1280, 720)
    fps = 144

    def __init__(self):
        self._observer_manager = ObserverManager(self)

        pygame.init()
        pygame.mixer.init()
        self._window = pygame.display.set_mode(self.resolution)
        self._clock = pygame.time.Clock()

        self._screen = None

        self._init_screen()
        self.run()

    @property
    def observer_manager(self) -> ObserverManager:
        return self._observer_manager

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def window(self):
        return self._window

    def change_screen(self, new_screen: Screen) -> None:
        old_screen = self._screen
        self._screen = new_screen

        self._observer_manager.on_change_screen(old_screen, new_screen)

    def run(self) -> None:
        while True:
            self.update()
            self.render()

    def update(self) -> None:
        elapsed_ms = self._clock.tick(self.fps)
        events = list(pygame.event.get())  # Events are passed in a list so that they can be consumed if necessary

        self._screen.update(elapsed_ms, events)
        AudioHandler.update(elapsed_ms)  # Audio is handled at the top level since it may persist between screens

    def render(self) -> None:
        updated_rects = self._screen.render(self._window)

        pygame.display.update(updated_rects)

    def _init_screen(self):
        ##### TODO: Replace with logic which loads a menu Screen

        state_extended_class = State.with_extensions(Registrar, Listeners)
        save_state = state_extended_class()
        StateHandler.register_paths(save_state)

        try:
            with open("save/save1.json", "r") as file:
                save_state.set(loads(file.read()))
        except FileNotFoundError:
            StateHandler.generate_new_save_data(save_state)

        self.change_screen(World(self, save_state))

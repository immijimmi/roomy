from pygame import Surface
from managedstate import State
from managedstate.extensions import Registrar

from abc import ABC
from typing import Optional

from ...handlers import HitboxHandler
from ..renderable import Renderable


class Screen(Renderable, ABC):
    """
    Any class that inherits from Screen should be used as a top-level object in the game loop.
    Different subclasses of Screen should represent different views of the game;
    for example, the main menu would be one Screen subclass whereas the game world would be a separate Screen subclass
    """

    def __init__(self, game, state: State.with_extensions(Registrar), surface: Optional[Surface] = None):
        super().__init__(game, surface=surface, render_position=(0, 0), parent=None, priority=None)

        self._state = state
        self._hitbox_handler = HitboxHandler()

        self.register_paths(self._state)

    @property
    def state(self) -> State.with_extensions(Registrar):
        return self._state

    @property
    def hitbox_handler(self) -> HitboxHandler:
        return self._hitbox_handler

    def _update(self, tick_number: int, elapsed_ms: int, input_events: list, *args, **kwargs) -> None:
        """
        This method can be further extended as necessary in subclasses
        """

        self._hitbox_handler.reset_checked_collisions()

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        """
        Can optionally be overridden.
        Register any paths for a state object which would be used by this screen or its children here
        """

        pass

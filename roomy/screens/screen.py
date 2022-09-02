from pygame import Surface
from managedstate import State
from managedstate.extensions import Registrar

from abc import ABC

from ..renderable import Renderable
from ..constants import Constants as GameConstants
from ..handlers import HitboxHandler


class Screen(Renderable, ABC):
    """
    Any class that inherits from Screen should be used as a top-level object in the game loop.
    Different derived classes of Screen are to represent different views of the game;
    for example, the start menu would be one Screen subclass whereas the game world would be a separate Screen subclass
    """

    def __init__(self, game, state: State.with_extensions(Registrar)):
        surface = Surface((game.window.get_width(), game.window.get_height()))
        surface.fill(GameConstants.COLOURS["dev"])

        super().__init__(game, surface=surface, position=(0, 0), parent=None, priority=None)

        self._state = state
        self._hitbox_handler = HitboxHandler()

        self.register_paths(self._state)

    @property
    def state(self) -> State.with_extensions(Registrar):
        return self._state

    @property
    def hitbox_handler(self) -> HitboxHandler:
        return self._hitbox_handler

    def _update(self, elapsed_ms: int, events: list):
        self._hitbox_handler.reset_checked_collisions()

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        """
        Can optionally be overridden.
        Register any paths for a state object which would be used by this screen or its children here
        """

        pass

from pygame import Surface

from abc import ABC

from ..entity import Entity
from ..constants import Constants as ClassConstants
from ..hitboxmanager import HitboxManager


class Screen(Entity, ABC):
    """
    A class that implements Screen is a top-level object in the game loop.
    Different derived classes of Screen should represent different views of the game;
    for example, the start menu would be one Screen class whereas the game world would be a separate Screen class
    """

    def __init__(self, game, state):
        position = (0, 0)
        surface = Surface((game.window.get_width(), game.window.get_height()))
        surface.fill(ClassConstants.COLOURS["dev"])

        super().__init__(game, state, surface=surface, position=position, parent=None, priority=None)

        self._hitbox_manager = HitboxManager(self)

    @property
    def hitbox_manager(self) -> HitboxManager:
        return self._hitbox_manager

    def _update(self, elapsed_ms: int, events: list):
        self._hitbox_manager.reset_checked_collisions()

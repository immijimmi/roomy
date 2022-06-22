from typing import Iterable
from abc import ABC
from weakref import ref

from ..tagged import Tagged
from .constants import Constants


class Hitbox(Tagged, ABC):
    def __init__(self, parent: "Entity.with_extensions(Hitboxed)", tags: Iterable[str]):
        super().__init__(tags)

        # Weakref so that it does not prevent parent entity being garbage collected
        self._parent_entity = ref(parent)

    @property
    def hitbox_manager(self) -> "HitboxManager":
        """
        Shortcut property which accesses the current game screen, and then the current hitbox manager through that
        """

        return self.parent_entity.game.screen.hitbox_manager

    @property
    def parent_entity(self) -> "Entity.with_extensions(Hitboxed)":
        return self._parent_entity()

    def is_collision(self, other: "Hitbox", check_by_entity: bool = True) -> bool:
        """
        Checks for a collision between this hitbox and the provided other hitbox.
        If this collision has already been checked this tick, returns False.

        If check_by_entity is True, hitbox objects that have the same parent Entity
        are considered to be the same hitbox for this purpose
        """

        if check_by_entity:
            collision_key = frozenset((self.parent_entity, other.parent_entity))
        else:
            collision_key = frozenset((self, other))

        if collision_key in self.hitbox_manager.checked_collisions:
            return False  # This collision check has already been carried out previously this tick

        self.hitbox_manager.checked_collisions.add(collision_key)
        return self._is_collision(other)

    def _is_collision(self, other: "Hitbox") -> bool:
        """
        This is an overridable method which should complete (or further delegate) the actual check for a collision
        between this hitbox object and the other provided hitbox object
        """

        raise NotImplementedError

    def _is_valid_tag(self, tag: str) -> bool:
        return tag in Constants.HITBOX_TAGS

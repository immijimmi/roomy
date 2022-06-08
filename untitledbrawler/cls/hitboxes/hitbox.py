from typing import Iterable, Optional
from abc import ABC
from weakref import ref

from ..tagged import Tagged
from .constants import Constants


class Hitbox(Tagged, ABC):
    def __init__(self, tags: Iterable[str], parent: Optional["Entity.with_extensions(Hitboxed)"] = None):
        super().__init__(tags)

        # Weakref so that it does not prevent parent object being garbage collected
        self._parent = lambda: None if parent is None else ref(parent)

    @property
    def parent(self) -> "Entity.with_extensions(Hitboxed)":
        return self._parent()

    def is_collision(self, other: "Hitbox", check_by_entity: bool = True) -> bool:
        """
        Checks for a collision between this hitbox and the provided other hitbox.
        If this collision has already been checked this tick, returns False.

        If check_by_entity is True, hitbox objects that have the same parent Entity
        are considered to be the same hitbox for this purpose
        """

        parent = self.parent
        other_parent = other.parent

        if not parent and not other_parent:
            # There is no accessible HitboxManager to log collision checks to
            return self._is_collision(other)

        hitbox_manager = (parent or other_parent).game.screen.hitbox_manager

        if check_by_entity:
            collision_key = frozenset((parent or self, other.parent or other))
        else:
            collision_key = frozenset((self, other))

        if collision_key in hitbox_manager.checked_collisions:
            return False  # This collision check has already been carried out previously this tick

        hitbox_manager.checked_collisions.add(collision_key)
        return self._is_collision(other)

    def _is_collision(self, other: "Hitbox") -> bool:
        """
        This is an overridable method which should complete (or further delegate) the actual check for a collision
        between this hitbox object and the other provided hitbox object
        """

        raise NotImplementedError

    def _is_valid_tag(self, tag: str) -> bool:
        return tag in Constants.HITBOX_TAGS

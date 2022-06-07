from typing import Iterable, Hashable, Optional, FrozenSet
from abc import ABC
from weakref import ref

from ..entity import Entity


class Hitbox(ABC):
    def __init__(self, tags: Iterable[Hashable], parent: Optional["Entity.with_extensions(Hitboxed)"] = None):
        self._tags: FrozenSet[Hashable] = frozenset(tags)

        # Weakref so that it does not prevent parent object being garbage collected
        self._parent = lambda: None if parent is None else ref(parent)

    @property
    def tags(self) -> FrozenSet[Hashable]:
        return self._tags

    @property
    def parent(self) -> "Entity.with_extensions(Hitboxed)":
        return self._parent()

    def is_collision(self, other: "Hitbox") -> bool:
        """
        Checks for a collision between this hitbox object and the provided other hitbox object.
        If this specific collision (i.e. between these two hitbox objects) has already been checked this tick,
        returns False
        """

        if parent := self.parent:
            collision_key = frozenset((self, other))
            checked_collisions = parent.game.screen.hitbox_manager.checked_collisions

            if collision_key in checked_collisions:
                return False  # This collision check has already been carried out previously this tick

            checked_collisions.add(collision_key)

        return self._is_collision(other)

    def is_any_collision(self, others: Iterable["Hitbox"]) -> bool:
        """
        Checks for a collision between this hitbox and at least one of the provided other hitbox objects - this uses
        the same general logic as its single-hitbox counterpart `.is_collision()`.
        If any collision is detected, all possible collisions this function call would have checked for
        are then marked as checked for this tick.

        This method is designed to be used by entities which have collision surfaces comprised of multiple hitboxes,
        where a collision with any one hitbox means a collision with the entity and so all its hitboxes
        should be marked as checked simultaneously
        """

        if parent := self.parent:
            collision_keys = [frozenset((self, other)) for other in others]
            checked_collisions = parent.game.screen.hitbox_manager.checked_collisions

            for collision_key in collision_keys:
                if collision_key in checked_collisions:
                    return False

            for collision_key in collision_keys:
                checked_collisions.add(collision_key)

        for other in others:
            if self._is_collision(other):
                return True

        return False

    def _is_collision(self, other: "Hitbox") -> bool:
        """
        This is an overridable method which should complete (or further delegate) the actual check for a collision
        between this object and the other provided object
        """

        raise NotImplementedError

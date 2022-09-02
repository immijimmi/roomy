from typing import Iterable
from abc import ABC
from weakref import ref

from ..tagged import Tagged
from .constants import Constants


class Hitbox(Tagged, ABC):
    def __init__(self, parent: "Renderable.with_extensions(Hitboxed)", tags: Iterable[str]):
        super().__init__(tags)

        # Weakref so that it does not prevent parent object being garbage collected
        self._parent_renderable = ref(parent)

    @property
    def hitbox_handler(self) -> "HitboxHandler":
        """
        Shortcut property which accesses the current game screen, and then the current hitbox handler through that
        """

        return self.parent_renderable.game.screen.hitbox_handler

    @property
    def parent_renderable(self) -> "Renderable.with_extensions(Hitboxed)":
        return self._parent_renderable()

    def is_collision(self, other: "Hitbox", check_by_parent: bool = True) -> bool:
        """
        Checks for a collision between this hitbox and the provided other hitbox.
        If this collision has already been checked this tick, returns False.

        If check_by_parent is True, hitbox objects that have the same parent Renderable
        are considered to be the same hitbox for this purpose
        """

        if check_by_parent:
            collision_key = frozenset((self.parent_renderable, other.parent_renderable))
        else:
            collision_key = frozenset((self, other))

        if collision_key in self.hitbox_handler.checked_collisions:
            return False  # This collision check has already been carried out previously this tick

        self.hitbox_handler.checked_collisions.add(collision_key)
        return self._is_collision(other)

    def _is_collision(self, other: "Hitbox") -> bool:
        """
        Must be overridden.
        Should complete (or further delegate, if necessary) the actual check for a collision
        between this hitbox object and the other provided hitbox object
        """

        raise NotImplementedError

    def _is_valid_tag(self, tag: str) -> bool:
        return tag in Constants.HITBOX_TAGS

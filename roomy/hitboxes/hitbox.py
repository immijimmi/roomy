from objectextensions import Decorators

from typing import Iterable, Dict, Type, Callable
from abc import ABC
from weakref import ref

from ..tagged import Tagged


class Hitbox(Tagged, ABC):
    @Decorators.classproperty
    def COLLISION_CHECKERS(cls) -> Dict[Type["Hitbox"], Callable[["Hitbox", "Hitbox"], bool]]:
        """
        When two hitboxes are being checked for a collision, at least one of the two Hitbox objects involved
        should have a compatible collision checker function stored in this property.
        It should be stored using the other involved hitbox's class as a key
        """

        raise NotImplementedError

    def __init__(self, parent: "Renderable.with_extensions(Hitboxed)", tags: Iterable[str] = ()):
        # Weakref so that it does not prevent parent object being garbage collected
        self._parent_renderable = ref(parent)

        super().__init__(tags)

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

        if type(other) in self.COLLISION_CHECKERS:
            self.hitbox_handler.checked_collisions.add(collision_key)

            return self.COLLISION_CHECKERS[type(other)](self, other)
        elif type(self) in other.COLLISION_CHECKERS:
            self.hitbox_handler.checked_collisions.add(collision_key)

            return other.COLLISION_CHECKERS[type(self)](self, other)
        else:
            raise TypeError(
                "unable to locate a compatible collision checker for a collision between "
                f"`{type(self).__name__}` and `{type(other).__name__}` instances"
            )

    def _is_valid_tag(self, tag: str) -> bool:
        return tag in self.parent_renderable.game.config.HITBOX_TAGS

from objectextensions import Extension

from typing import Iterable, FrozenSet
from abc import ABC

from ...renderables import Renderable
from ...hitboxes import Hitbox


class Hitboxed(Extension, ABC):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Renderable)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Hitboxed.__wrap_init)

        Extension._set_property(target_cls, "hitboxes", Hitboxed.__hitboxes)
        Extension._set_setter(target_cls, "hitboxes", "hitboxes", Hitboxed.__set_hitboxes)

        Extension._set(target_cls, "generate_hitboxes", Hitboxed.__generate_hitboxes)
        Extension._set(target_cls, "check_collisions", Hitboxed.__check_collisions)
        Extension._set(target_cls, "collide", Hitboxed.__collide)

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_hitboxes", frozenset())
        self.hitboxes = self.generate_hitboxes()

    def __hitboxes(self) -> FrozenSet[Hitbox]:
        return self._hitboxes

    def __set_hitboxes(self, hitboxes: Iterable[Hitbox]):
        hitbox_manager = self.game.screen.hitbox_manager

        for hitbox in self._hitboxes:
            if hitbox not in hitboxes:
                hitbox_manager.remove(hitbox)

        for hitbox in hitboxes:
            if hitbox not in self._hitboxes:
                hitbox_manager.add(hitbox)

        self._hitboxes = frozenset(hitboxes)

    def __generate_hitboxes(self) -> Iterable[Hitbox]:
        """
        Must be overridden.
        Should return new, correct hitboxes for this Renderable object based on its current state.
        Note that hitboxes for this object may still be created outside of this method on an ad-hoc basis
        (e.g. in response to specific events)
        """

        raise NotImplementedError

    def __check_collisions(self) -> None:
        """
        Can optionally be overridden.
        Standardises the entry point for checking collisions for this Renderable object.

        Hitboxes from other Renderable objects that may have valid collisions with this one's hitboxes can be retrieved
        using the get() method on self.game.screen.hitbox_manager, filtered down via the optional parameters
        that method can receive.

        When a collision is detected between two objects, each of their respective `.collide()` methods should
        be invoked and passed the other object involved in that collision.
        """

        pass

    def __collide(self, other: "Renderable.with_extensions(Hitboxed)") -> None:
        """
        Can optionally be overridden.
        Any on-collision effects applied by and to this and the other provided Renderable object should be
        implemented in one of their `.collide()` methods

        This includes inspecting the other renderable to decide what effects should apply, if necessary.

        When a collision is detected and this method is invoked, it should *also* be invoked on the other object
        involved in the collision and passed this object as an argument
        to allow both objects' collision logic to be applied
        """

        pass

from objectextensions import Extension

from typing import Iterable, FrozenSet

from ...entity import Entity
from ...hitboxes import Hitbox


class Hitboxed(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

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
        hitbox_handler = self.game.screen.hitbox_handler

        for hitbox in self._hitboxes:
            if hitbox not in hitboxes:
                hitbox_handler.remove(hitbox)

        for hitbox in hitboxes:
            if hitbox not in self._hitboxes:
                hitbox_handler.add(hitbox)

        self._hitboxes = frozenset(hitboxes)

    def __generate_hitboxes(self) -> Iterable[Hitbox]:
        """
        Must be overridden.
        Should return the correct hitboxes for this entity based on its current state.
        Note that hitboxes can still be created elsewhere on an ad-hoc basis (e.g. in response to specific events)
        """

        raise NotImplementedError

    def __check_collisions(self) -> None:
        """
        Can optionally be overridden.
        Standardises the entry point for checking collisions for this entity.

        Hitboxes from other entities that may have valid collisions with this entity's hitboxes can be retrieved
        using the get() method on self.game.screen.hitbox_handler, filtered down via the optional parameters
        that method can receive.

        When a collision is detected between two entities, each of their respective collide() methods should be
        invoked here and passed the other entity involved in that collision.
        """

        pass

    def __collide(self, other: "Entity.with_extensions(Hitboxed)") -> None:
        """
        Can optionally be overridden.
        Should apply this entity's on-collision effects to itself and/or the provided other entity.

        This includes inspecting the other entity (if needed) to decide what effects should apply.

        - Any *direct* changes to the position or movement (or other stats) of an entity as a result of the collision
          itself should be handled by that entity, not by the other involved entity
        """

        pass

from objectextensions import Extension

from typing import Iterable

from ..entity import Entity
from ..hitboxes import Hitbox


class Hitboxed(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Hitboxed.__wrap_init)
        Extension._wrap(target_cls, "update", Hitboxed.__wrap_update)

        Extension._set(target_cls, "generate_default_hitboxes", Hitboxed.__generate_default_hitboxes)
        Extension._set(target_cls, "set_hitboxes", Hitboxed.__set_hitboxes)
        Extension._set(target_cls, "check_collisions", Hitboxed.__check_collisions)
        Extension._set(target_cls, "collide", Hitboxed.__collide)

    def __generate_default_hitboxes(self) -> Iterable[Hitbox]:
        """
        Must be overridden in subclasses with a method that provides a valid hitbox
        """

        raise NotImplementedError

    def __set_hitboxes(self, hitboxes: Iterable[Hitbox]) -> None:
        """
        Workaround method since objectextensions does not currently support binding properties
        """

        hitbox_manager = self.game.screen.hitbox_manager

        for hitbox in self._hitboxes:
            if hitbox not in hitboxes:
                hitbox_manager.remove(hitbox)

        for hitbox in hitboxes:
            if hitbox not in self._hitboxes:
                hitbox_manager.add(hitbox)

        self._hitboxes = frozenset(hitboxes)

    def __check_collisions(self) -> None:
        """
        Overridable lifecycle method to standardise the entry point for collision checking.

        Hitboxes from other entities that may have valid collisions with this entity's hitboxes can be retrieved
        using the get() method on self.game.screen.hitbox_manager, filtered down via the optional parameters
        that method may receive.

        When a collision is detected between two entities, each of their respective collide() methods should be
        invoked and passed the other entity involved in that collision.
        """

        pass

    def __collide(self, other: "Entity.with_extensions(Hitboxed)"):
        """
        Overridable method which should apply this entity's on-collision effects
        to itself and/or the provided other entity.
        This includes inspecting the other entity (if needed) to decide what effects should apply.

        - Any *direct* changes to the position or movement (or other stats) of an entity as a result of the collision
          itself should be handled by that entity, not by the other involved entity
        """

        pass

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_hitboxes", frozenset())

        self.set_hitboxes(self.generate_default_hitboxes())

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.check_collisions()

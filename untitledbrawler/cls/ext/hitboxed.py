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
        Overridable lifecycle method to standardise the entry point for collision checking
        """

        pass

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_hitboxes", frozenset())

        self.set_hitboxes(self.generate_default_hitboxes())

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.check_collisions()

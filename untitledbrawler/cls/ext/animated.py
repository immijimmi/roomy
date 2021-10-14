from objectextensions import Extension

from ..entity import Entity
from ..animations import Animation


class Animated(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Animated.__wrap_init)
        Extension._wrap(target_cls, "update", Animated.__wrap_update)

        Extension._set(target_cls, "get_default_animation", Animated.__generate_default_animation)

    def __generate_default_animation(self) -> Animation:
        """
        Must be overridden in subclasses with a method that provides a valid animation
        """

        raise NotImplementedError

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "animation", self.get_default_animation())

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.animation.update(elapsed_ms)
        self.surface = self.animation.frame

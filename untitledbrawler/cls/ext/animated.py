from objectextensions import Extension

from ..entity import Entity
from ..animations import RepeatAnimation


class Animated(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Animated.__wrap_init)
        Extension._wrap(target_cls, "update", Animated.__wrap_update)

        Extension._set(target_cls, "default_animation_key", Animated.__default_animation_key)

    @property
    def __default_animation_key(self) -> str:
        """
        .default_animation_key must be overridden in the subclass with a property that provides a valid animation key
        """

        raise NotImplementedError

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "animation", RepeatAnimation(self, self.default_animation_key))

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.animation.update(elapsed_ms)
        self.surface = self.animation.frame

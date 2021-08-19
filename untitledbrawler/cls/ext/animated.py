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

    def __wrap_init(self, *args, **kwargs):
        Extension._set(self, "animation", RepeatAnimation(self))  # Default animation will be a repeating idle animation
        yield

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.animation.update(elapsed_ms)
        self.surface = self.animation.frame

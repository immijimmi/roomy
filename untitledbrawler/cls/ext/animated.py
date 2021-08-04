from objectextensions import Extension

from ..entity import Entity
from ..animation import Animation
from ..data import AnimationHandler


class Animated(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Animated.__wrap_init)
        Extension._wrap(target_cls, "update", Animated.__wrap_update)

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "animation", Animation(self))

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.animation.add_elapsed(elapsed_ms)
        self.animation.update()

        self.surface = AnimationHandler.get_frame(self)

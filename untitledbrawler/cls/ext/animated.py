from objectextensions import Extension

from ..entity import Entity
from ..animation import Animation
from ..data import AnimationHandler


class Animated(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Animated.__wrap_init)
        Extension._wrap(target_cls, "update", Animated.__wrap_update)

    def __wrap_init(self, *args, **kwargs):
        Extension._set(self, "animation", Animation(self))
        yield

    def __wrap_update(self, elapsed_ms, events):
        yield
        self.animation.add_elapsed(elapsed_ms)
        self.animation.update()

        self.surface = AnimationHandler.get_frame(self)

    # Not in use as objectextensions does not yet support property syntax
    @property
    def __animation_getter(self):
        return self._animation

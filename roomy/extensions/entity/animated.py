from objectextensions import Extension

from ...entity import Entity
from ...animations import Animation


class Animated(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Entity)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Animated.__wrap_init)

        Extension._set_property(target_cls, "animation", Animated.__animation)
        Extension._set_setter(target_cls, "animation", "animation", Animated.__apply_animation)

        Extension._wrap(target_cls, "update", Animated.__wrap_update)
        Extension._set(target_cls, "generate_animation", Animated.__generate_animation)

    def __wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_animation", self.generate_animation())

    def __animation(self) -> Animation:
        return self._animation

    def __apply_animation(self, animation: Animation):
        """
        Named 'apply' rather than 'set' because it is not guaranteed that the provided animation will be set,
        if it is lower priority than the current animation
        """

        if animation.priority >= self._animation.priority:
            self._animation = animation

    def __wrap_update(self, elapsed_ms, events):
        yield
        self._animation.update(elapsed_ms)
        self.surface = self._animation.frame

    def __generate_animation(self) -> Animation:
        """
        Must be overridden.
        Should return the correct animation for this entity based on its current state.
        Note that animations can still be created elsewhere on an ad-hoc basis (e.g. in response to specific events)
        """

        raise NotImplementedError

from typing import Any
from datetime import timedelta


class Animation:
    default_frame_time = timedelta(microseconds=20000)

    def __init__(
            self, parent: "Entity.with_extensions(Animated)",
            animation_key: str = "", frame_time: timedelta = default_frame_time, priority: Any = None,
            speed: float = 1, repeats: bool = True
    ):
        self._set(parent, animation_key, frame_time, priority, speed, repeats)

    @property
    def parent(self) -> "Entity.with_extensions(Animated)":
        return self._parent

    @property
    def key(self) -> Any:
        return self._key

    @property
    def frame_time(self) -> timedelta:
        return self._frame_time

    @property
    def priority(self) -> Any:
        return self._priority

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def repeats(self) -> bool:
        return self._repeats

    @property
    def elapsed(self) -> timedelta:
        return self._elapsed

    @property
    def elapsed_effective(self) -> timedelta:
        """
        This property tracks elapsed time with animation speed accounted for,
        so that the speed can be changed at any time without causing the animation to lose its correct progress
        """

        return self._elapsed_effective

    def add_elapsed(self, elapsed_ms: int):
        elapsed = timedelta(microseconds=elapsed_ms*1000)
        effective_elapsed = elapsed * self._speed

        self._elapsed += elapsed
        self._elapsed_effective += effective_elapsed

    def update(self) -> None:
        """
        This method should validate the animation's status - if the animation is considered expired upon validation,
        it should take the surplus elapsed duration and apply it to a fresh Animation with default or inherited
        init params (which should represent an idle animation), and call .set() with that animation
        """

        pass  ##### TODO

    def set(self, animation: "Animation"):
        if animation.priority >= self._priority:
            self._set(
                animation.parent,
                animation.key, animation.frame_time, animation.priority,
                animation.speed, animation.repeats
            )

            self._elapsed = animation.elapsed
            self._elapsed_effective = animation.elapsed_effective

    def _set(self, parent, animation_key, frame_time, priority, speed, repeats):
        self._parent = parent
        self._key = animation_key
        self._frame_time = frame_time
        self._priority = priority
        self._speed = speed
        self._repeats = repeats

        self._elapsed = timedelta(0)
        self._elapsed_effective = timedelta(0)

from typing import Any
from datetime import timedelta


class Animation:
    default_frame_time = timedelta(microseconds=20000)

    def __init__(
            self, parent: "Entity.with_extensions(Animated)",
            animation_key: str = "", frame_time: timedelta = default_frame_time, priority: Any = None,
            speed: float = 1, on_finish: str = "repeat"
    ):
        self._set(parent, animation_key, frame_time, priority, speed, on_finish)

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
    def on_finish(self) -> str:
        """
        Determines what should happen at the end of the animation
        (AnimationHandler implements the different behaviours)
        """

        return self._on_finish

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

    def set(self, animation: "Animation"):
        if animation.priority >= self._priority:
            self._set(
                animation.parent,
                animation.key, animation.frame_time, animation.priority,
                animation.speed, animation.on_finish
            )

            self._elapsed = animation.elapsed
            self._elapsed_effective = animation.elapsed_effective

    def _set(self, parent, animation_key, frame_time, priority, speed, on_finish):
        assert on_finish in ("", "", "")

        self._parent = parent
        self._key = animation_key
        self._frame_time = frame_time
        self._priority = priority
        self._speed = speed
        self._on_finish = on_finish

        self._elapsed = timedelta(0)
        self._elapsed_effective = timedelta(0)

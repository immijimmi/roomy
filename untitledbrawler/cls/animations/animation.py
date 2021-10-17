from typing import Any
from datetime import timedelta
from abc import ABC
from weakref import ref

from pygame import Surface

from ..data import AnimationHandler
from .constants import AnimationParams


class Animation(ABC):
    default_frame_duration = timedelta(microseconds=20000)

    def __init__(
            self, parent: "Entity.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None
    ):
        self._parent = ref(parent)  # Weakref so that it does not prevent parent object being garbage collected
        self._key = animation_key
        self._speed = speed
        self._size = size
        self._priority = priority

        self._data = AnimationHandler.get_data(type(parent), animation_key)

        self._elapsed = timedelta(0)
        self._elapsed_effective = timedelta(0)

    @property
    def parent(self) -> "Entity.with_extensions(Animated)":
        return self._parent()

    @property
    def key(self) -> Any:
        return self._key

    @property
    def size(self) -> float:
        return self._size

    @size.setter
    def size(self, value: float):
        self._size = value

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = value

    @property
    def priority(self) -> Any:
        return self._priority

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

    @property
    def total_frames(self) -> int:
        return len(self._data[AnimationParams.FRAMES])

    @property
    def frame(self) -> Surface:
        frame_file_path = self._data[AnimationParams.FRAMES][self.frame_index]

        return AnimationHandler.get_frame(frame_file_path, self._size)

    @property
    def frame_index(self) -> int:
        raise NotImplementedError

    def update(self, elapsed_ms: int):
        self._add_elapsed(elapsed_ms)
        self._update()

    def _update(self):
        """
        Any additional work that may be needed in specific animations can be completed here
        """

        pass

    def _add_elapsed(self, elapsed_ms: int):
        elapsed = timedelta(microseconds=elapsed_ms*1000)
        effective_elapsed = elapsed * self._speed

        self._elapsed += elapsed
        self._elapsed_effective += effective_elapsed

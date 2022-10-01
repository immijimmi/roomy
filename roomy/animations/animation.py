from typing import Any
from datetime import timedelta
from abc import ABC
from weakref import ref

from pygame import Surface

from ..handlers.enums import AnimationDataKey


class Animation(ABC):
    default_frame_duration = timedelta(microseconds=20000)

    def __init__(
            self, parent: "Renderable.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None
    ):
        self.size: float = size
        self.speed: float = speed

        self._parent_renderable = ref(parent)  # Weakref so that it does not prevent parent object being garbage collected
        self._key = animation_key
        self._priority = priority

        self._settings = self.animation_handler.get_settings(type(parent), animation_key)

        self._elapsed = timedelta(0)
        self._elapsed_effective = timedelta(0)

    @property
    def parent_renderable(self) -> "Renderable.with_extensions(Animated)":
        return self._parent_renderable()

    @property
    def animation_handler(self):
        """
        Shortcut property which accesses the current game screen, and then the current animation handler through that
        """

        return self.parent_renderable.game.animation_handler

    @property
    def key(self) -> str:
        return self._key

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
        return len(self._settings[AnimationDataKey.FRAMES])

    @property
    def frame(self) -> Surface:
        frame_key = self._settings[AnimationDataKey.FRAMES][self.frame_index]

        return self.animation_handler.get_frame(frame_key, self.size)

    @property
    def frame_index(self) -> int:
        raise NotImplementedError

    def update(self, elapsed_ms: int):
        self._add_elapsed(elapsed_ms)
        self._update()

    def _update(self):
        """
        Any additional work that may be needed in specific animations,
        including playing sounds at specific parts of the animation, can be completed here
        """

        pass

    def _add_elapsed(self, elapsed_ms: int):
        elapsed = timedelta(microseconds=elapsed_ms*1000)
        effective_elapsed = elapsed * self.speed

        self._elapsed += elapsed
        self._elapsed_effective += effective_elapsed

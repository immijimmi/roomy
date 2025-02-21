from pygame import Surface

from typing import Any
from datetime import timedelta
from abc import ABC
from weakref import ref


class Animation(ABC):
    def __init__(
            self, parent: "Renderable.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None
    ):
        self.size: float = size
        self.speed: float = speed

        self._parent_renderable = ref(parent)  # Weakref so that it does not prevent parent object being garbage collected
        self._key = animation_key
        self._priority = priority

        self._elapsed = timedelta(0)
        self._elapsed_effective = timedelta(0)

    @property
    def parent_renderable(self) -> "Renderable.with_extensions(Animated)":
        return self._parent_renderable()

    @property
    def animation_cache(self):
        """
        Shortcut property which accesses the current game screen, and then the game's animation cache through that
        """

        return self.parent_renderable.game.animation_cache

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
    def frame(self) -> Surface:
        """
        Must be overridden with a property that returns a Surface representing
        the current frame of the animation, based on its current state
        """

        raise NotImplementedError

    def update(self, elapsed_ms: int) -> None:
        self._add_elapsed(elapsed_ms)
        self._update(elapsed_ms)

    def _update(self, elapsed_ms: int) -> None:
        """
        Lifecycle method, called automatically each game tick.
        Can optionally be overridden.

        Any additional work that may be needed in specific animations,
        including playing sounds at specific parts of the animation, can be completed here
        """

        pass

    def _add_elapsed(self, elapsed_ms: int) -> None:
        elapsed = timedelta(microseconds=elapsed_ms*1000)
        effective_elapsed = elapsed * self.speed

        self._elapsed += elapsed
        self._elapsed_effective += effective_elapsed

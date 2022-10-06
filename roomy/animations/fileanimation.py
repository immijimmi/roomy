from pygame import Surface

from abc import ABC
from typing import Any

from ..handlers.enums import AnimationDataKey
from .animation import Animation


class FileAnimation(Animation, ABC):
    def __init__(
            self, parent: "Renderable.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None
    ):
        super().__init__(parent, animation_key, size=size, speed=speed, priority=priority)

        self._settings = self.animation_handler.get_settings(type(parent), animation_key)

    @property
    def total_frames(self) -> int:
        return len(self._settings[AnimationDataKey.FRAMES])

    @property
    def frame(self) -> Surface:
        frame_key = self._settings[AnimationDataKey.FRAMES][self.frame_index]

        return self.animation_handler.get_frame(frame_key, self.size)

    @property
    def frame_index(self) -> int:
        """
        Must be overridden with a property that returns the index for
        the current frame of the animation, based on its current state
        """

        raise NotImplementedError

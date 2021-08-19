from typing import Any, Optional
from datetime import timedelta

from .animation import Animation


class RepeatAnimation(Animation):
    def __init__(
            self, parent: "Entity.with_extensions(Animated)",
            animation_key: str = "", speed: float = 1, priority: Any = None,
            frame_duration: Optional[timedelta] = None
    ):
        super().__init__(parent, animation_key, speed, priority)

        self._frame_time = frame_duration or self._data.get("frame_duration", None) or Animation.default_frame_duration

    @property
    def frame_index(self):
        frames_elapsed = int(self._elapsed_effective / self._frame_time)

        return frames_elapsed % self.total_frames

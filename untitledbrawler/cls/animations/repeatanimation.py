from typing import Any, Optional
from datetime import timedelta

from .animation import Animation
from .constants import AnimationParams


class RepeatAnimation(Animation):
    def __init__(
            self, parent: "Entity.with_extensions(Animated)", animation_key: str,
            speed: float = 1, priority: Any = None,
            frame_duration: Optional[timedelta] = None
    ):
        super().__init__(parent, animation_key, speed, priority)

        if frame_duration is not None:
            self._frame_time = frame_duration
        else:
            frame_duration_ms = self._data.get(AnimationParams.FRAME_DURATION_MS, None)

            if frame_duration_ms is not None:
                self._frame_time = timedelta(microseconds=frame_duration_ms*1000)
            else:
                self._frame_time = Animation.default_frame_duration

    @property
    def frame_index(self):
        frames_elapsed = int(self._elapsed_effective / self._frame_time)

        return frames_elapsed % self.total_frames

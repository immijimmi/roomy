from typing import Any, Optional
from datetime import timedelta

from .animation import Animation
from ..handlers.enums import AnimationDataKey


class RepeatAnimation(Animation):
    def __init__(
            self, parent: "Entity.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None,
            frame_duration: Optional[timedelta] = None,
            windup_frames: int = 0
    ):
        super().__init__(parent, animation_key, size=size, speed=speed, priority=priority)

        # Windup frames are optional non-repeating frames at the start of the animation
        self._windup_frames = windup_frames

        if frame_duration is not None:
            self._frame_time = frame_duration
        else:
            frame_duration_ms = self._settings.get(AnimationDataKey.FRAME_DURATION_MS, None)

            if frame_duration_ms is not None:
                self._frame_time = timedelta(microseconds=frame_duration_ms*1000)
            else:
                self._frame_time = Animation.default_frame_duration

    @property
    def windup_frames(self) -> int:
        return self._windup_frames

    @property
    def frame_index(self):
        frames_elapsed = int(self._elapsed_effective / self._frame_time)

        if frames_elapsed < self._windup_frames:
            return frames_elapsed
        else:
            return (
                           (frames_elapsed - self._windup_frames) %
                           (self.total_frames - self._windup_frames)
                   ) + self._windup_frames

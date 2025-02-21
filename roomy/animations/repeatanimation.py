from typing import Any, Optional
from datetime import timedelta

from .fileanimation import FileAnimation
from ..utils.enums import AnimationDataKey


class RepeatAnimation(FileAnimation):
    def __init__(
            self, parent: "Renderable.with_extensions(Animated)", animation_key: str,
            size: float = 1, speed: float = 1, priority: Any = None,
            fps: Optional[float] = None, windup_frames: int = 0
    ):
        super().__init__(parent, animation_key, size=size, speed=speed, priority=priority)

        if fps is None:
            fps = self._settings.get(AnimationDataKey.DEFAULT_FPS, None)
        if fps is None:
            fps = self.parent_renderable.game.config.ANIMATION_DEFAULT_FPS

        self._fps = fps
        self._frame_time = timedelta(microseconds=(10**6)/fps)

        # Windup frames are optional non-repeating frames at the start of the animation
        self._windup_frames = windup_frames

    @property
    def fps(self) -> float:
        """
        This property does not factor in animation speed; it is the base framerate of the animation only
        """

        return self._fps

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

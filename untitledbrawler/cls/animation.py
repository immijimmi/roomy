from typing import Any
from datetime import timedelta


class Animation:
    def __init__(
            self, parent: "Entity.with_extensions(Animated)",
            animation_key: str = "", frame_time: timedelta = timedelta(microseconds=20000),
            repeats: bool = True
    ):
        self._parent = parent
        self._key = animation_key
        self._frame_time = frame_time
        self._repeats = repeats

        self._elapsed = timedelta(0)

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
    def repeats(self) -> bool:
        return self._repeats

    @property
    def elapsed(self) -> timedelta:
        return self._elapsed

    def add_elapsed(self, elapsed_ms: int):
        self._elapsed += timedelta(microseconds=elapsed_ms*1000)

    def update(self) -> None:
        """
        This method should validate the animation's status - if the animation is considered expired upon validation,
        it should take the surplus elapsed duration and apply it to a fresh Animation with no other
        init params (which should represent an idle animation), and assign that to the .animation attribute of the
        parent instance to replace this animation
        """

        pass  ##### TODO

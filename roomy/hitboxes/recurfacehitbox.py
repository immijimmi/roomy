from objectextensions import Decorators

from typing import Dict, Type, Callable, Iterable

from .hitbox import Hitbox


class RecurfaceHitbox(Hitbox):
    def __init__(self, parent: "Renderable.with_extensions(Hitboxed)", tags: Iterable[str] = (), is_inverted: bool = False):
        super().__init__(parent, tags=tags)

        self._is_inverted = is_inverted

    @property
    def is_inverted(self) -> bool:
        return self._is_inverted

    @Decorators.classproperty
    def COLLISION_CHECKERS(cls) -> Dict[Type[Hitbox], Callable[[Hitbox, Hitbox], bool]]:
        return {
            cls: cls._is_collision_recurfacehitbox
        }

    @staticmethod
    def _is_collision_recurfacehitbox(a: "RecurfaceHitbox", b: "RecurfaceHitbox") -> bool:
        a_absolute_position = a.parent_renderable.absolute_render_position
        b_absolute_position = b.parent_renderable.absolute_render_position

        a_left, a_right = (
            a_absolute_position[0],
            a_absolute_position[0] + a.parent_renderable.surface.get_width()
        )
        a_top, a_bottom = (
            a_absolute_position[1],
            a_absolute_position[1] + a.parent_renderable.surface.get_height()
        )

        b_left, b_right = (
            b_absolute_position[0],
            b_absolute_position[0] + b.parent_renderable.surface.get_width()
        )
        b_top, b_bottom = (
            b_absolute_position[1],
            b_absolute_position[1] + b.parent_renderable.surface.get_height()
        )

        if a.is_inverted and b.is_inverted:
            return True
        elif a.is_inverted and (not b.is_inverted):
            return (
                    (b_left < a_left) or (b_right > a_right) or
                    (b_top < a_top) or (b_bottom > a_bottom)
            )
        elif (not a.is_inverted) and b.is_inverted:
            return (
                    (a_left < b_left) or (a_right > b_right) or
                    (a_top < b_top) or (a_bottom > b_bottom)
            )
        else:
            return (
                    (a_left < b_right) and (b_left < a_right) and
                    (a_top < b_bottom) and (b_top < a_bottom)
            )

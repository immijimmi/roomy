from objectextensions import Decorators

from typing import Dict, Type, Callable

from .hitbox import Hitbox


class RecurfaceHitbox(Hitbox):
    @Decorators.classproperty
    def COLLISION_CHECKERS(cls) -> Dict[Type["Hitbox"], Callable[["Hitbox", "Hitbox"], bool]]:
        return {
            cls: cls._is_collision_recurfacehitbox
        }

    @staticmethod
    def _is_collision_recurfacehitbox(a: Hitbox, b: Hitbox) -> bool:
        a_x_bounds = (
            a.parent_renderable.x_render_position,
            a.parent_renderable.x_render_position + a.parent_renderable.surface.get_width()
        )
        a_y_bounds = (
            a.parent_renderable.y_render_position,
            a.parent_renderable.y_render_position + a.parent_renderable.surface.get_height()
        )

        b_x_bounds = (
            b.parent_renderable.x_render_position,
            b.parent_renderable.x_render_position + b.parent_renderable.surface.get_width()
        )
        b_y_bounds = (
            b.parent_renderable.y_render_position,
            b.parent_renderable.y_render_position + b.parent_renderable.surface.get_height()
        )

        return (
                (a_x_bounds[0] < b_x_bounds[1]) and (b_x_bounds[0] < a_x_bounds[1]) and
                (a_y_bounds[0] < b_y_bounds[1]) and (b_y_bounds[0] < a_y_bounds[1])
        )

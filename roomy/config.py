from pygame import event

from typing import Callable, Iterable, Dict, Container

from .renderables import RenderableHitboxTag


class Config:
    TICK_RATE: float = 120  # Number of game ticks per second. A value of 0 indicates unlimited tick rate (must be >=0)
    """
    Please note that while unlimited tick rate is supported, any parts of the game state
    which are updated per tick may behave differently in a given period of real time at different tick rates.
    It is therefore highly recommended to keep the tick rate locked to a static value (>0)
    """
    FPS: float = 0  # A value of 0 indicates unlimited framerate (must be >=0)

    GET_INPUT_EVENTS: Callable[[], Iterable] = event.get

    RESOURCE_FOLDER_PATH = "res"  # Can either be absolute, or relative to the current working directory

    CUSTOM_CLASSES: Dict[str, type] = {}

    # Should contain all possible valid tags for the Hitbox class
    HITBOX_TAGS: Container = set(
        attribute.value for attribute in RenderableHitboxTag
    )

    ANIMATION_DEFAULT_FPS: float = 24

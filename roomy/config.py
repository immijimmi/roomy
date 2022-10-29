from pygame import event

from typing import Callable, Iterable, Dict, Container

from .renderables import RenderableHitboxTag


class Config:
    TICK_RATE: float = 144  # Number of game ticks per second. A value of 0 indicates unlimited tick rate
    """
    Please note that while unlimited tick rate is supported, any parts of the game state
    which are updated per tick may behave differently at different tick rates.
    It is therefore recommended to lock the tick rate to a specific value
    """
    FPS: float = 0  # A value of 0 indicates unlimited framerate

    GET_INPUT_EVENTS: Callable[[], Iterable] = event.get

    RESOURCE_FOLDER_PATH = "res"  # Can either be absolute, or relative to the current working directory

    CUSTOM_CLASSES: Dict[str, type] = {}

    # Should contain all possible valid tags for the Hitbox class
    HITBOX_TAGS: Container = set(
        attribute.value for attribute in RenderableHitboxTag
    )

    ANIMATION_DEFAULT_FPS: float = 50

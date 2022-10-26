from pygame import event

from typing import Callable, Iterable, Dict, Container

from .renderables import RenderableHitboxTag


class Config:
    FPS: float = 0  # A value of 0 indicates unlimited framerate
    UPDATES_PER_FRAME: int = 1
    GET_INPUT_EVENTS: Callable[[], Iterable] = event.get

    RESOURCE_FOLDER_PATH = "res"  # Can either be absolute, or relative to the current working directory

    CUSTOM_CLASSES: Dict[str, type] = {}

    # Should contain all possible valid tags for the Hitbox class
    HITBOX_TAGS: Container = set(
        attribute.value for attribute in RenderableHitboxTag
    )

    ANIMATION_DEFAULT_FPS: float = 50

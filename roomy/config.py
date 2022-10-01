from pygame import event

from typing import Callable, Iterable, Dict, Container


class Config:
    FPS: int = 0  # A value of 0 indicates unlimited framerate
    UPDATES_PER_FRAME: int = 1
    GET_INPUT_EVENTS: Callable[[], Iterable] = event.get

    RESOURCE_FOLDER_PATH = "res"  # Can either be absolute, or relative to the current working directory

    CUSTOM_CLASSES: Dict[str, type] = {}

    HITBOX_TAGS: Container = set()  # Should contain all possible valid tags for the Hitbox class

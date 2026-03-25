from typing import Dict, Container

from .renderables.enums import RenderableHitboxTag


class Config:
    # Number of physics ticks per second
    TICK_RATE: float = 60  # A value of 0 indicates unlimited tick rate (must be >=0)
    """
    Please note that while unlimited tick rate is supported, it is not recommended as game physics will behave
    unpredictably
    """
    FPS: float = 0  # A value of 0 indicates unlimited framerate (must be >=0)

    RESOURCE_FOLDER_PATH = "res"  # Can either be absolute, or relative to the current working directory

    # Classes stored here will be stored in the class registrar
    CUSTOM_CLASSES: Dict[str, type] = {}
    # Determines whether the class registrar should search the global namespace, as a last resort
    ALLOW_GLOBAL_CUSTOM_CLASSES: bool = True

    # Should contain all possible valid tags for the Hitbox class
    HITBOX_TAGS: Container = set(
        attribute for attribute in RenderableHitboxTag
    )

    ANIMATION_DEFAULT_FPS: float = 24

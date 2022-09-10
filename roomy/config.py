from typing import Dict, Container


class Config:
    CUSTOM_CLASSES: Dict[str, type] = {}

    HITBOX_TAGS: Container = set()  # Should contain all possible valid tags for the Hitbox class

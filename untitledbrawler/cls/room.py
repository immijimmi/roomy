from typing import Any

from .entity import Entity
from .ext import Animated
from .animations import RepeatAnimation


class Room(Entity.with_extensions(Animated)):
    def __init__(self, room_id: Any, world: "World"):
        self._room_id = room_id  # Hoisted as it is required for animation setup in the base constructor

        super().__init__(position=(0, 0))

        self.parent = world

        self._register_paths()
        self._load_room()

    @property
    def room_id(self) -> Any:
        return self._room_id

    @property
    def default_animation_key(self):
        # Room animation keys will simply be stringified IDs
        return str(self._room_id)

    def _load_room(self):
        pass  ##### TODO

    def _register_paths(self):
        pass

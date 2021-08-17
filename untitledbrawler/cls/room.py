from typing import Any

from .entity import Entity
from .ext import Animated


class Room(Entity.with_extensions(Animated)):
    def __init__(self, room_id: Any, world: "World"):
        super().__init__(position=(0, 0))

        self.room_id = room_id
        self.parent = world

        self._register_paths()
        self._load_room()

    def _update(self, elapsed_ms, events):
        pass

    def _load_room(self):
        pass  ##### TODO

    def _register_paths(self):
        pass

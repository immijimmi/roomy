from typing import Any

from .methods import Methods
from .entity import Entity
from .ext import Animated
from .roomoccupants import RoomOccupant


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
        room_contents_data = self.parent.state.registered_get("room_contents", [self._room_id])

        for room_occupant_class_name in room_contents_data:
            occupant_class: RoomOccupant = Methods.get_class_from_str(room_occupant_class_name)

            for occupant_kwargs in room_contents_data[room_occupant_class_name]:
                self.add_child(occupant_class(self, **occupant_kwargs))

        ##### TODO: Add logic to render players in the room as well - player data will be separate from room data

    def _register_paths(self):
        pass

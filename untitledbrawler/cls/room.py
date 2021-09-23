from typing import Any, Iterable

from .methods import Methods
from .entity import Entity
from .ext import Animated
from .roomoccupants import RoomOccupant


class Room(Entity.with_extensions(Animated)):
    def __init__(self, room_id: Any, world: "World"):
        self._room_id = room_id  # Hoisted as it is required for animation setup in the base constructor

        super().__init__(position=(0, 0))

        self.parent = world

        self._load_room()

    @property
    def room_id(self) -> Any:
        return self._room_id

    @property
    def default_animation_key(self):
        # Room animation keys will simply be stringified IDs
        return str(self._room_id)

    def _load_room(self):
        curr_room_occupants_ids: Iterable[str] = self.parent.state.registered_get("room_occupants_ids", [self._room_id])
        curr_players_ids: Iterable[str] = self.parent.state.registered_get("curr_players_ids")

        for room_occupant_id in curr_room_occupants_ids:
            room_occupant_data: dict = self.parent.state.registered_get("room_occupant", [room_occupant_id])

            occupant_class: RoomOccupant = Methods.get_class_from_str(room_occupant_data["class"])
            occupant_stats: dict = room_occupant_data["stats"]

            self.add_child(occupant_class(self, stats=occupant_stats))

        for player_id in curr_players_ids:
            player_data: dict = self.parent.state.registered_get("player", [player_id])

            player_class: RoomOccupant = Methods.get_class_from_str(player_data["class"])
            player_stats: dict = player_data["stats"]

            self.add_child(player_class(self, stats=player_stats))

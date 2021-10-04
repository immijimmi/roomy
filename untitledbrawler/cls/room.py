from pygame import transform, image

from typing import Iterable

from .methods import Methods
from .entity import Entity
from .roomoccupants import RoomOccupant


class Room(Entity):
    def __init__(self, game, room_id: str):
        super().__init__(game, position=(0, 0))

        self._room_id = room_id

        self._load_surface()
        self._load_room()

    @property
    def room_id(self) -> str:
        return self._room_id

    def _load_surface(self, size: float = 1):
        world = self.game.screen
        background_key = world.state.registered_get("room_background_key", [self._room_id])

        background_file_path = rf"untitledbrawler\res\{type(self)}\{background_key}.png"
        self.surface = transform.rotozoom(image.load(background_file_path).convert_alpha(), 0, size)

    def _load_room(self):
        world = self.game.screen

        curr_room_occupants_ids: Iterable[str] = world.state.registered_get("room_occupants_ids", [self._room_id])
        curr_players_ids: Iterable[str] = world.state.registered_get("curr_players_ids")

        for room_occupant_id in curr_room_occupants_ids:
            room_occupant_data: dict = world.state.registered_get("room_occupant", [room_occupant_id])

            occupant_class: RoomOccupant = Methods.get_class_from_str(room_occupant_data["class"])
            occupant_stats: dict = room_occupant_data["stats"]

            self.add_child(occupant_class(self, **occupant_stats))

        for player_id in curr_players_ids:
            player_data: dict = world.state.registered_get("player", [player_id])

            player_class: RoomOccupant = Methods.get_class_from_str(player_data["class"])
            player_stats: dict = player_data["stats"]

            self.add_child(player_class(self, **player_stats))

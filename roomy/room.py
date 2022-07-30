from pygame import transform, image
from managedstate import State
from managedstate.extensions import Registrar

from typing import Iterable
from os import path

from .roomoccupants import *
from .methods import Methods
from .entity import Entity
from .constants import Constants


class Room(Entity):
    """
    Concrete class tightly coupled to the World screen, which renders a single room and its occupants
    """

    def __init__(self, parent: "World", room_id: str):
        super().__init__(parent.game, parent=parent, position=(0, 0), priority=0)

        self._room_id = room_id

        self._load_surface()
        self._load_room()

    @property
    def state(self) -> State.with_extensions(Registrar):
        """
        Shortcut property which accesses the state attached to the parent World object
        """

        return self.parent_recurface.state

    @property
    def room_id(self) -> str:
        return self._room_id

    def _load_surface(self, size: float = 1):
        """
        Loads the background image for the room object. Assumes a standard location for the image file as
        dictated below in background_file_path
        """

        background_key = self.state.registered_get("room_background_key", [self._room_id])
        background_file_path = path.join(
            Constants.RESOURCE_FOLDER_PATH,
            f"{type(self).__name__}",
            f"{background_key}.png"
        )

        surface = image.load(background_file_path).convert_alpha()
        surface = transform.rotozoom(surface, 0, size)
        self.surface = surface

    def _load_room(self):
        """
        Instantiates all the entities present in the current room.
        Assumes that any classes listed in the game's state are available under the same name in the global namespace;
        for example, `from .test import Test` would make a class "Test" available for this purpose
        """

        curr_room_occupants_ids: Iterable[str] = self.state.registered_get("room_occupants_ids", [self._room_id])
        curr_players_ids: Iterable[str] = self.state.registered_get("curr_players_ids")

        for room_occupant_id in curr_room_occupants_ids:
            room_occupant_data: dict = self.state.registered_get("room_occupant", [room_occupant_id])

            occupant_class: RoomOccupant = Methods.get_obj_by_str_name(room_occupant_data["class"])
            occupant_stats: dict = room_occupant_data["stats"]

            occupant_class(self, **occupant_stats)

        for player_id in curr_players_ids:
            player_data: dict = self.state.registered_get("player", [player_id])

            player_class: RoomOccupant = Methods.get_obj_by_str_name(player_data["class"])
            player_stats: dict = player_data["stats"]

            player_class(self, **player_stats)

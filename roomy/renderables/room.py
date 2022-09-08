from pygame import transform, image

from typing import Type, Tuple, List
from os import path

from ..methods import Methods
from ..constants import Constants as GameConstants
from .renderable import Renderable
from .entity import Entity
from .enums import EntityDataKeys


class Room(Renderable):
    """
    Concrete class tightly coupled to the World screen, which renders a single room and its occupants.
    Can be subclassed as needed to add further functionality
    """

    def __init__(self, parent: "World", room_id: str):
        super().__init__(parent.game, parent=parent, position=(0, 0), priority=0)

        self._room_id = room_id

        self._load_surface()
        self._load_room()

    @property
    def room_id(self) -> str:
        return self._room_id

    def _load_surface(self, size: float = 1):
        """
        Loads the background image for the room object. Assumes a standard location for the image file as
        dictated below in `background_file_path`
        """

        background_id = self.parent_recurface.state.registered_get("room_background_id", [self._room_id])
        background_file_path = path.join(
            GameConstants.RESOURCE_FOLDER_PATH,
            f"{type(self).__name__}",
            f"{background_id}.png"
        )

        surface = image.load(background_file_path).convert_alpha()
        surface = transform.rotozoom(surface, 0, size)
        self.surface = surface

    def _load_room(self):
        """
        Instantiates all the entities present in the current room.
        Assumes that any Entity subclasses listed in the game's state
        are available under the same name in your global namespace
        """

        curr_room_entities_ids: List[str] = self.parent_recurface.state.registered_get(
            "room_entities_ids", [self._room_id]
        )

        for entity_id in curr_room_entities_ids:
            entity_data: dict = self.parent_recurface.state.registered_get("entity", [entity_id])

            entity_class: Type[Entity] = Methods.get_obj_by_str_name(entity_data[EntityDataKeys.CLASS])
            entity_details: Tuple[list, dict] = (entity_data[EntityDataKeys.ARGS], entity_data[EntityDataKeys.KWARGS])

            entity_class(self, *entity_details[0], **entity_details[1])

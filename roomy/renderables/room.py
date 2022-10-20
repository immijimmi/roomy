from typing import Type, Tuple, List
from os import path

from ..methods import Methods
from .renderable import Renderable
from .entity import Entity
from .enums import EntityDataKey


class Room(Renderable):
    """
    Concrete class tightly coupled to the World screen, which renders a single room and its occupants.
    Can be subclassed as needed to add further functionality
    """

    def __init__(self, parent: "World", room_id: str):
        super().__init__(parent.game, parent=parent, render_position=(0, 0), priority=0)

        self._room_id = room_id
        self.surface = self._generate_surface()

        self._is_loaded = False

    @property
    def room_id(self) -> str:
        return self._room_id

    def _update(self, elapsed_ms: int, input_events: list, *args, **kwargs) -> None:
        if not self._is_loaded:
            self._load_room()

            self._is_loaded = True

    def _generate_surface(self):
        """
        Loads the background image for the room object as a new Surface.
        Assumes a standard location for the image file as dictated below in `background_file_path`
        """

        background_file_path = path.join(
            self.game.config.RESOURCE_FOLDER_PATH,
            self.game.screen.state.registered_get("room_background_file_path", [self._room_id])
        )

        return Methods.load_image(background_file_path)

    def _load_room(self):
        """
        Instantiates all the entities present in the current room.
        Assumes that any custom Entity subclasses listed in the game's state
        have been made available to the game's CustomClassHandler
        """

        curr_room_entities_ids: List[str] = self.game.screen.state.registered_get(
            "room_entities_ids", [self._room_id]
        )

        for entity_id in curr_room_entities_ids:
            entity_data: dict = self.game.screen.state.registered_get("entity", [entity_id])

            entity_class: Type[Entity] = self.game.custom_class_handler.get(entity_data[EntityDataKey.CLASS])
            entity_details: Tuple[list, dict] = (
                entity_data.get(EntityDataKey.ARGS, []),
                entity_data.get(EntityDataKey.KWARGS, {})
            )

            entity_class(self, *entity_details[0], **entity_details[1])

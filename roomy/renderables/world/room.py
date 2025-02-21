from typing import List, Type
from os import path

from ...extensions import Hitboxed
from ...hitboxes import RecurfaceHitbox
from ...methods import Methods
from ..renderable import Renderable
from .enums import RenderableHitboxTag, RenderableDataKey


class Room(Renderable.with_extensions(Hitboxed)):
    """
    Concrete class used by the World screen, which renders a single room and its occupants.
    Can be subclassed as needed to add further functionality
    """

    def __init__(self, parent: "World", room_id: str):
        super().__init__(parent.game, parent=parent, render_position=(0, 0), priority=0)

        self._room_id = room_id
        self.surface = self._generate_surface()

        self._load_room()

    @property
    def room_id(self) -> str:
        return self._room_id

    def generate_hitboxes(self):
        return [RecurfaceHitbox(self, tags=(RenderableHitboxTag.ROOM, ), is_inverted=True)]

    def check_collisions(self) -> None:
        """
        This class explicitly does not check for collisions with other objects.
        Other objects may check for collisions with this object as needed, and act accordingly if
        a collision is detected
        """

        pass

    def collide(self, other: Renderable.with_extensions(Hitboxed)) -> None:
        """
        This class explicitly does not apply any on-collision effects. Any that are necessary should be
        applied by the other colliding object
        """

        pass

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
        Instantiates all the occupants of the current room.
        Assumes that any custom classes listed in the game's state
        have been made available to the game's CustomClassHandler
        """

        curr_room_occupants_ids: List[str] = self.game.screen.state.registered_get(
            "room_occupants_ids", [self._room_id]
        )

        for occupant_id in curr_room_occupants_ids:
            occupant_data: dict = self.game.screen.state.registered_get("room_occupant", [occupant_id])

            occupant_class: Type[Renderable] = self.game.custom_class_handler.get(
                occupant_data[RenderableDataKey.CLASS]
            )
            occupant_args: list = occupant_data.get(RenderableDataKey.ARGS, [])
            occupant_kwargs: dict = occupant_data.get(RenderableDataKey.KWARGS, {})

            occupant_class(self, *occupant_args, **occupant_kwargs)

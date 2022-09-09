from managedstate import State
from managedstate.extensions import Registrar
from managedstate.extensions.registrar import PartialQueries

from .screen import Screen
from ..room import Room
from ..methods import Methods as RenderablesMethods
from ...handlers import EventKey


class World(Screen):
    """
    A concrete implementation of Screen, that represents a standard room-based game world
    """

    def __init__(self, game, state: State.with_extensions(Registrar)):
        super().__init__(game, state)

        self._register_concrete_classes()

        self._curr_room = None
        self.set_room()

        ##### TODO: Render UI layer after room

    @property
    def curr_room(self) -> Room:
        return self._curr_room

    def set_room(self) -> None:
        """
        Assumes that any Room subclasses listed in the game's state
        are available under the same name in your global namespace (in __main__)
        """

        new_room_id = self.state.registered_get("current_room_id")
        old_room = self._curr_room
        old_room_id = None if old_room is None else old_room.room_id

        if new_room_id == old_room_id:
            return

        with self.game.listener_handler.surrounding_events(
                EventKey.WILL_CHANGE_ROOM, EventKey.DID_CHANGE_ROOM,
                self._curr_room, new_room_id
        ):
            new_room_cls = RenderablesMethods.get_obj_by_str_name(
                self.state.registered_get("room_class", [new_room_id])
            )
            new_room = new_room_cls(self, new_room_id)

            self._curr_room = new_room

            if old_room is not None:
                old_room.parent_recurface = None

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        state.register_path("current_room_id", ["current_room_id"], [str(None)])

        state.register_path("entity", ["entities", PartialQueries.KEY], [{}, {}])

        state.register_path("room", ["rooms", PartialQueries.KEY], [{}, {}])
        state.register_path("room_class", ["rooms", PartialQueries.KEY, "class"], [{}, {}, "Room"])
        state.register_path("room_entities_ids", ["rooms", PartialQueries.KEY, "entities_ids"], [{}, {}, []])
        state.register_path(
            "room_background_id",
            ["rooms", PartialQueries.KEY, "background_id"],
            [{}, {}, str(None)]
        )

    @staticmethod
    def _register_concrete_classes():
        RenderablesMethods.REGISTERED_OBJECTS.update({"Room": Room})

from managedstate import State
from managedstate.extensions import Registrar
from managedstate.extensions.registrar import PartialQueries

from .screen import Screen
from ..room import Room


class World(Screen):
    """
    A concrete implementation of Screen, that represents a standard room-based game world
    """

    def __init__(self, game, state: State.with_extensions(Registrar)):
        super().__init__(game, state)

        self._curr_room = None
        self.set_room()

        ##### TODO: Render UI layer after room

    @property
    def curr_room(self) -> Room:
        return self._curr_room

    def set_room(self) -> None:
        new_room_id = self.state.registered_get("current_room_id")

        if self.curr_room is None:
            pass
        elif new_room_id == self.curr_room.room_id:
            return

        old_room = self._curr_room
        self._curr_room = Room(self, new_room_id)

        old_room.parent_recurface = None
        self.game.observer_handler.on_change_room(old_room, self.curr_room)

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        state.register_path("current_room_id", ["current_room_id"], [str(None)])

        state.register_path("entity", ["entities", PartialQueries.KEY], [{}, {}])

        state.register_path("room", ["rooms", PartialQueries.KEY], [{}, {}])
        state.register_path("room_entities_ids", ["rooms", PartialQueries.KEY, "entities_ids"], [{}, {}, []])
        state.register_path(
            "room_background_id",
            ["rooms", PartialQueries.KEY, "background_id"],
            [{}, {}, str(None)]
        )

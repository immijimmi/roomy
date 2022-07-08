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
        new_room_id = self.state.registered_get("curr_room_id")

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
        state.register("curr_room_id", ["current", "room_id"], [{}, str(None)])
        state.register("curr_players_ids", ["current", "players_ids"], [{}, []])

        state.register("player", ["players", PartialQueries.KEY], [{}, {}])
        state.register("room", ["rooms", PartialQueries.KEY], [{}, {}])
        state.register("room_occupant", ["room_occupants", PartialQueries.KEY], [{}, {}])

        state.register("room_occupants_ids", ["rooms", PartialQueries.KEY, "occupants_ids"], [{}, {}, []])
        state.register(
            "room_background_key",
            ["rooms", PartialQueries.KEY, "background_key"],
            [{}, {}, str(None)]
        )

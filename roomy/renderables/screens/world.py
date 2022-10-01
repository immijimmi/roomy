from managedstate import State
from managedstate.extensions import Registrar
from managedstate.extensions.registrar import PartialQueries

from .screen import Screen
from ..room import Room
from ...handlers import GameEventKey


class World(Screen):
    """
    A concrete implementation of Screen, that represents a standard room-based game world
    """

    def __init__(self, game, state: State.with_extensions(Registrar)):
        super().__init__(game, state)

        # Registering a class `Room` which may appear in the game state and which would be needed inside this class
        self.game.custom_class_handler.update({"Room": Room})

        self._current_room = None

        # TODO: Render UI layer after room

    @property
    def curr_room(self) -> Room:
        return self._current_room

    def set_room(self) -> None:
        """
        Checks what room ID the current room should have via the game's state, and if it does not match
        the room ID of the room that is currently active, a new room with the correct room ID is initialised
        and swapped in.

        This method can be manually invoked in order to apply a room change immediately, but this is not strictly
        necessary - when the room ID is changed in the game's state, on the next call to .update() this method will be
        automatically invoked.

        This method assumes that any custom Room subclasses listed in the game's state
        have been made available to the game's CustomClassHandler
        """

        state_current_room_id = self.state.registered_get("current_room_id")
        current_room_id = None if self._current_room is None else self._current_room.room_id

        if state_current_room_id == current_room_id:
            return

        with self.game.game_event_handler(GameEventKey.CHANGE_ROOM, self._current_room, state_current_room_id):
            old_room = self._current_room

            new_room_cls = self.game.custom_class_handler.get(
                self.state.registered_get("room_class", [state_current_room_id])
            )
            new_room = new_room_cls(self, state_current_room_id)

            self._current_room = new_room

            if old_room is not None:
                old_room.parent_recurface = None

    def _update(self, elapsed_ms: int, input_events: list):
        super()._update(elapsed_ms, input_events)

        self.set_room()

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        state.register_path("current_room_id", ["current_room_id"], [str(None)])

        state.register_path("entity", ["entities", PartialQueries.KEY], [{}, {}])

        state.register_path("room", ["rooms", PartialQueries.KEY], [{}, {}])
        state.register_path("room_class", ["rooms", PartialQueries.KEY, "class"], [{}, {}, "Room"])
        state.register_path("room_entities_ids", ["rooms", PartialQueries.KEY, "entities_ids"], [{}, {}, []])
        state.register_path(
            "room_background_file_path",
            ["rooms", PartialQueries.KEY, "background_file_path"],
            [{}, {}, f"{str(None)}.png"]
        )

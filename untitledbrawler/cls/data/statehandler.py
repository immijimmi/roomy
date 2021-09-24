from managedstate import State
from managedstate.extensions import Registrar

from .constants import Constants


class StateHandler:
    """
    Helper class responsible for any generation of the game state.
    """

    ROOM_STATES = {  # Initial room states used for worldgen. All IDs are to be strings
        str(None): {}
    }

    @staticmethod
    def generate_new_save_data(save_state: State.with_extensions(Registrar)):
        StateHandler._register_paths(save_state)

        StateHandler._generate_rooms(save_state)
        ##### TODO: Incomplate. All initial worldgen will be in here

    @staticmethod
    def _generate_rooms(save_state: State.with_extensions(Registrar)):
        for room_id in StateHandler.ROOM_STATES:
            room_state = StateHandler.ROOM_STATES[room_id]
            save_state.registered_set(room_state, "room", [room_id])

    @staticmethod
    def _register_paths(save_state: State.with_extensions(Registrar)):
        save_state.register("curr_room_id", ["current", "room_id"], [{}, str(None)])
        save_state.register("curr_players_ids", ["current", "players_ids"], [{}, []])

        save_state.register("player", ["players", Constants.PATH_DYNAMIC_KEY], [{}, {}])
        save_state.register("room", ["rooms", Constants.PATH_DYNAMIC_KEY], [{}, {}])
        save_state.register("room_occupant", ["room_occupants", Constants.PATH_DYNAMIC_KEY], [{}, {}])

        save_state.register("room_occupants_ids", ["rooms", Constants.PATH_DYNAMIC_KEY, "occupants_ids"], [{}, {}, []])

from managedstate import State
from managedstate.extensions import Registrar


class StateHandler:
    """
    Helper class responsible for any generation of the game state.
    """

    ROOM_STATES = {  # Initial room states used for worldgen. All IDs are to be strings
        str(None): {
            "occupants_ids": [],
            "background_key": str(None)
        }
    }


    @staticmethod
    def generate_new_save_data(save_state: State.with_extensions(Registrar)):
        StateHandler._generate_room_occupants(save_state)
        StateHandler._generate_rooms(save_state)

        ##### TODO: Incomplete. All initial worldgen will be in here

    @staticmethod
    def _generate_rooms(save_state):
        for room_id in StateHandler.ROOM_STATES:
            room_state = StateHandler.ROOM_STATES[room_id]
            save_state.registered_set(room_state, "room", [room_id])

    @staticmethod
    def _generate_room_occupants(save_state):
        pass

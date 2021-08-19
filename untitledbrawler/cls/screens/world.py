from managedstate import State

from .screen import Screen
from ..room import Room


class World(Screen):
    def __init__(self, game: "Game", state: State):
        super().__init__(game)

        self.state = state
        self.curr_room = None

        self._register_paths()
        self.set_room()

    def set_room(self):
        new_room_id = self.state.registered_get("curr_room_id")

        if self.curr_room is None:
            pass
        elif new_room_id == self.curr_room.room_id:
            return

        old_room = self.curr_room
        self.curr_room = Room(new_room_id, self)

        self.game.observers.on_change_room(old_room, self.curr_room)

    def _register_paths(self):
        self.state.register("curr_room_id", ["curr_room_id"], [None])

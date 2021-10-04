from managedstate import State

from .screen import Screen
from ..room import Room


class World(Screen):
    def __init__(self, game: "Game", state: State):
        super().__init__(game)

        self._state = state
        self._curr_room = None

        self.set_room()

    @property
    def state(self) -> State:
        return self._state

    @property
    def curr_room(self) -> Room:
        return self._curr_room

    def set_room(self):
        new_room_id = self.state.registered_get("curr_room_id")

        if self.curr_room is None:
            pass
        elif new_room_id == self.curr_room.room_id:
            return

        old_room = self._curr_room
        self._curr_room = Room(self.game, new_room_id)

        self.game.observers.on_change_room(old_room, self.curr_room)

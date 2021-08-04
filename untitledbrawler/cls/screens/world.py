from managedstate import State

from .screen import Screen
from ..room import Room


class World(Screen):
    def __init__(self, game: "Game", state: State):
        super().__init__(game)

        self.state = state
        self.curr_room = None

        self.change_room(Room(self))  ##### TODO

    def change_room(self, new_room: Room):
        old_room = self.curr_room
        self.curr_room = new_room

        self.game.observers.on_change_room(old_room, new_room)

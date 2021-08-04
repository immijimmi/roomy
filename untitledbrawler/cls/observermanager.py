from typing import Callable

from .screens import Screen
from .room import Room


class RemoveObserver(Exception):
    pass


class ObserverManager:
    def __init__(self, game: "Game"):
        self._game = game

        self._registered = {
            "on_change_screen": set(),
            "on_change_room": set(),
        }

    @property
    def game(self) -> "Game":
        return self._game

    def add(self, event_key: str, observer: Callable) -> None:
        self._registered[event_key].add(observer)

    def remove(self, event_key: str, observer: Callable) -> None:
        self._registered[event_key].remove(observer)

    def on_change_screen(self, old_screen: Screen, new_screen: Screen) -> None:
        for observer in self._registered["on_change_screen"]:
            try:
                observer(old_screen, new_screen)
            except RemoveObserver:
                self.remove("on_change_screen", observer)

    def on_change_room(self, old_room: Room, new_room: Room) -> None:
        for observer in self._registered["on_change_room"]:
            try:
                observer(old_room, new_room)
            except RemoveObserver:
                self.remove("on_change_screen", observer)

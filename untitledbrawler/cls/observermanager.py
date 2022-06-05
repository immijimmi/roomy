from typing import Callable

from .screens import Screen
from .room import Room


class RemoveObserver(Exception):
    pass


class ObserverManager:
    REGISTERED = {
        "on_change_screen": set(),
        "on_change_room": set(),
    }

    @staticmethod
    def add(event_key: str, observer: Callable) -> None:
        ObserverManager.REGISTERED[event_key].add(observer)

    @staticmethod
    def remove(event_key: str, observer: Callable) -> None:
        ObserverManager.REGISTERED[event_key].remove(observer)

    @staticmethod
    def on_change_screen(old_screen: Screen, new_screen: Screen) -> None:
        for observer in ObserverManager.REGISTERED["on_change_screen"]:
            try:
                observer(old_screen, new_screen)
            except RemoveObserver:
                ObserverManager.remove("on_change_screen", observer)

    @staticmethod
    def on_change_room(old_room: Room, new_room: Room) -> None:
        for observer in ObserverManager.REGISTERED["on_change_room"]:
            try:
                observer(old_room, new_room)
            except RemoveObserver:
                ObserverManager.remove("on_change_screen", observer)

from typing import Callable
from contextlib import contextmanager


class RemoveObserver(Exception):
    pass


class ObserverHandler:
    REGISTERED = {}

    @staticmethod
    def register(event_key: str, observer: Callable) -> None:
        ObserverHandler.REGISTERED.setdefault(event_key, set()).add(observer)

    @staticmethod
    def remove(event_key: str, observer: Callable) -> None:
        ObserverHandler.REGISTERED.setdefault(event_key, set()).remove(observer)

    @staticmethod
    def on_event(event_key: str, *args, **kwargs) -> None:
        observers_to_remove = set()

        for observer in ObserverHandler.REGISTERED.get(event_key, set()):
            try:
                observer(*args, **kwargs)
            except RemoveObserver:
                observers_to_remove.add(observer)

        for observer in observers_to_remove:
            ObserverHandler.remove(event_key, observer)

    @staticmethod
    @contextmanager
    def surrounding_events(before_event_key: str, after_event_key: str, *args, **kwargs):
        ObserverHandler.on_event(before_event_key, *args, **kwargs)
        yield
        ObserverHandler.on_event(after_event_key, *args, **kwargs)

from typing import Callable
from contextlib import contextmanager


class RemoveListener(Exception):
    pass


class ListenerHandler:
    REGISTERED = {}

    @staticmethod
    def register(event_key: str, listener: Callable) -> None:
        ListenerHandler.REGISTERED.setdefault(event_key, set()).add(listener)

    @staticmethod
    def remove(event_key: str, listener: Callable) -> None:
        ListenerHandler.REGISTERED.setdefault(event_key, set()).remove(listener)

    @staticmethod
    def on_event(event_key: str, *args, **kwargs) -> None:
        listeners_to_remove = set()

        for listener in ListenerHandler.REGISTERED.get(event_key, set()):
            try:
                listener(*args, **kwargs)
            except RemoveListener:
                listeners_to_remove.add(listener)

        for listener in listeners_to_remove:
            ListenerHandler.remove(event_key, listener)

    @staticmethod
    @contextmanager
    def surrounding_events(before_event_key: str, after_event_key: str, *args, **kwargs):
        ListenerHandler.on_event(before_event_key, *args, **kwargs)
        yield
        ListenerHandler.on_event(after_event_key, *args, **kwargs)

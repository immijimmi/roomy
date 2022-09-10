from typing import Callable, Union, Tuple, Literal
from contextlib import contextmanager


class RemoveListener(Exception):
    pass


class EventHandler:
    def __init__(self):
        self._listeners = {}

    @contextmanager
    def __call__(self, event_type: str, *args, **kwargs):
        self.on_event(("before", event_type), *args, **kwargs)
        yield
        self.on_event(("after", event_type), *args, **kwargs)

    def add_listener(self, event_key: Union[str, Tuple[Literal["before", "after"], str]], listener: Callable) -> None:
        self._listeners.setdefault(event_key, set()).add(listener)

    def remove_listener(self, event_key: Union[str, Tuple[Literal["before", "after"], str]], listener: Callable) -> None:
        self._listeners.setdefault(event_key, set()).remove(listener)

    def on_event(self, event_key: Union[str, Tuple[Literal["before", "after"], str]], *args, **kwargs) -> None:
        listeners_to_remove = set()

        for listener in self._listeners.get(event_key, set()):
            try:
                listener(*args, **kwargs)
            except RemoveListener:
                listeners_to_remove.add(listener)

        for listener in listeners_to_remove:
            self.remove_listener(event_key, listener)

from typing import Callable, Union, Tuple, Literal, Optional
from contextlib import contextmanager


class RemoveListener(Exception):
    pass


class EventHandler:
    """
    This class is responsible for notifying any registered listeners when an event is triggered.

    Listeners are categorised using an event key, which is either a string representing event type, or
    a tuple containing two strings (the first being either "before" or "after" and the second representing event type).
    A tuple event key such as this would be generated when using this class as a contextmanager;
    in such a case, .on_event() is invoked both before and after the event logic contained in the `with` block, with
    the appropriate tuple being passed as an event key each time.

    Alternatively, event key can be omitted when adding (or removing) a listener, to indicate that the listener
    should be notified on all events
    """

    def __init__(self):
        self._listeners = {}

    @contextmanager
    def __call__(self, event_type: str, *args, **kwargs):
        self.on_event(("before", event_type), *args, **kwargs)
        yield
        self.on_event(("after", event_type), *args, **kwargs)

    def add_listener(
            self, listener: Callable,
            event_key: Optional[Union[str, Tuple[Literal["before", "after"], str]]] = None
    ) -> None:
        self._listeners.setdefault(event_key, set()).add(listener)

    def remove_listener(
            self, listener: Callable,
            event_key: Optional[Union[str, Tuple[Literal["before", "after"], str]]] = None
    ) -> None:
        self._listeners.setdefault(event_key, set()).remove(listener)

    def on_event(self, event_key: Union[str, Tuple[Literal["before", "after"], str]], *args, **kwargs) -> None:
        # Notify listeners registered to all events
        listeners_to_remove = set()
        for listener in self._listeners.get(None, set()):
            try:
                listener(None, *args, **kwargs)
            except RemoveListener:
                listeners_to_remove.add(listener)

        for listener in listeners_to_remove:
            self.remove_listener(listener, None)

        # Notify listeners registered specifically to this event
        listeners_to_remove = set()
        for listener in self._listeners.get(event_key, set()):
            try:
                listener(event_key, *args, **kwargs)
            except RemoveListener:
                listeners_to_remove.add(listener)

        for listener in listeners_to_remove:
            self.remove_listener(listener, event_key)

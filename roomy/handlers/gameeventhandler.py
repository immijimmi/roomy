from typing import Callable, Union, Tuple, Literal, Optional
from contextlib import contextmanager


class RemoveListener(Exception):
    pass


class GameEventHandler:
    """
    This class is responsible for notifying any registered listeners when a game event is triggered.
    Game events can be anything related to a change in the game's state (for example - changing the current room,
    a character dying, a spell being cast etc.) and are triggered by calling .on_event()
    with the relevant event_key and any other related information for that event.

    Listeners are categorised by event_key, which is either a string representing the type of event occurring, or
    a tuple containing two strings (the first being either "before" or "after" and the second representing event type).
    A tuple event key such as this will be generated when using this class as a contextmanager;
    in such a case, .on_event() is invoked both before and after the event logic contained in the `with` block, with
    the appropriate tuple being passed as an event key each time.

    Any listener added via only a string for the event type, and not under these tuple variants
    for that same event type, will still be notified when the event is triggered using the above contextmanager.

    Alternatively, event_key can be omitted when adding (or removing) a listener, to indicate that the listener
    should be notified on all events
    """

    def __init__(self):
        self._listeners = {}

    @contextmanager
    def __call__(self, event_type: str, *args, **kwargs):
        self.on_event(("before", event_type), *args, **kwargs)
        yield
        """
        Both the non-specific and the after-specific variants of the event key are passed into `.on_event()` here,
        because any listener stored under the non-specific key should still be called at some point when
        calling listeners stored under the more specific variants (since the relevant event has still taken place)
        """
        self.on_event(event_type, *args, **kwargs)
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

from typing import Callable, Union, Tuple, Literal, Optional
from contextlib import contextmanager


class RemoveCallback(Exception):
    pass


class GameEventHandler:
    """
    This class is responsible for notifying any registered callback functions when a game event is triggered.
    Game events can be anything related to a change in the game's state (for example - changing the current room,
    a character dying, a spell being cast etc.) and are triggered by calling .on_event()
    with the relevant event_key and any other related information for that event.

    Callbacks are categorised by event_key, which is either a string representing the type of event occurring, or
    a tuple containing two strings (the first being either "before" or "after" and the second representing event type).
    A tuple event key such as this will be generated when using this class as a contextmanager;
    in such a case, .on_event() is invoked both before and after the event logic contained in the `with` block, with
    the appropriate tuple being passed as an event key each time.

    Any callback added via only a string for the event type, and not under these tuple variants
    for that same event type, will still be notified when the event is triggered using the above contextmanager.

    Alternatively, event_key can be omitted when adding (or removing) a callback, to indicate that the callback
    should be notified on all events.

    Additional information passed to callbacks when an event is triggered may be mutable, meaning that
    it can be made possible to modify events from within callbacks if necessary
    (although this capability should be used with caution)
    """

    def __init__(self):
        self._callbacks = {}

    @contextmanager
    def __call__(self, event_type: str, *args, **kwargs):
        self.on_event(("before", event_type), *args, **kwargs)
        yield
        """
        Both the non-specific and the "after"-specific variants of the event key are passed into `.on_event()` here,
        because any callback stored under the non-specific key should still be called at some point when
        invoking callbacks stored under the more specific variants (since the relevant event has still taken place)
        """
        self.on_event(event_type, *args, **kwargs)
        self.on_event(("after", event_type), *args, **kwargs)

    def add_callback(
            self, callback: Callable,
            event_key: Optional[Union[str, Tuple[Literal["before", "after"], str]]] = None
    ) -> None:
        self._callbacks.setdefault(event_key, set()).add(callback)

    def remove_callback(
            self, callback: Callable,
            event_key: Optional[Union[str, Tuple[Literal["before", "after"], str]]] = None
    ) -> None:
        self._callbacks.setdefault(event_key, set()).remove(callback)

    def on_event(self, event_key: Union[str, Tuple[Literal["before", "after"], str]], *args, **kwargs) -> None:
        # Notify callbacks registered to all events
        callbacks_to_remove = set()
        for callback in self._callbacks.get(None, set()):
            try:
                callback(None, *args, **kwargs)
            except RemoveCallback:
                callbacks_to_remove.add(callback)

        for callback in callbacks_to_remove:
            self.remove_callback(callback, None)

        # Notify callbacks registered specifically to this event
        callbacks_to_remove = set()
        for callback in self._callbacks.get(event_key, set()):
            try:
                callback(event_key, *args, **kwargs)
            except RemoveCallback:
                callbacks_to_remove.add(callback)

        for callback in callbacks_to_remove:
            self.remove_callback(callback, event_key)

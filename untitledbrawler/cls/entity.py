from recurfaces import Recurface
from objectextensions import Extendable
from pygame import Surface

from abc import ABC
from typing import Optional, Sequence, Any

from .data import AudioHandler


class Entity(Extendable, Recurface, ABC):
    """
    An Entity is any object that has a place in the rendering hierarchy.

    Explanation of additional constructor param requirements:
    - game: A reference to the Game instance allows all entities to navigate the object hierarchy from a static origin
    - state: Passed to all Entity objects for convenience in accessing the state object
    """

    def __init__(
            self, game: "Game", state: "State.with_extensions(Registrar)",
            parent: Optional["Entity"] = None, surface: Optional[Surface] = None,
            position: Optional[Sequence[int]] = None, priority: Any = None
    ):
        Extendable.__init__(self)
        Recurface.__init__(self, surface=surface, parent=parent, position=position, priority=priority)

        self._game = game
        self._state = state

    @property
    def game(self):
        return self._game

    @property
    def state(self):
        return self._state

    def update(self, elapsed_ms: int, events: list):
        self._update(elapsed_ms, events)

        child: Entity
        for child in reversed(self.ordered_child_recurfaces):  # Events passed to high render_priority children first
            child.update(elapsed_ms, events)

    def _update(self, elapsed_ms: int, events: list):
        """
        This is an overridable lifecycle method which will be called automatically in the game loop
        """

        pass

    def __del__(self):
        AudioHandler.delist_by_entity(self)

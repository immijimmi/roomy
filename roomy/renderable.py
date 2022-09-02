from recurfaces import Recurface
from objectextensions import Extendable
from pygame import Surface

from abc import ABC
from typing import Optional, Tuple, Any


class Renderable(Extendable, Recurface, ABC):
    """
    A Renderable object is any object that has a place in the rendering hierarchy.

    Explanation of additional constructor param requirements:
    - game: A reference to the Game instance allows all entities to navigate the object hierarchy from a static origin
    """

    def __init__(
            self, game: "Game",
            parent: Optional["Renderable"] = None, surface: Optional[Surface] = None,
            position: Optional[Tuple[int, int]] = None, priority: Any = None
    ):
        Extendable.__init__(self)
        Recurface.__init__(self, surface=surface, parent=parent, position=position, priority=priority)

        self._game = game

    @property
    def game(self):
        return self._game

    def update(self, elapsed_ms: int, events: list):
        self._update(elapsed_ms, events)

        child: Renderable
        for child in reversed(self.ordered_child_recurfaces):  # Events passed to high render_priority children first
            child.update(elapsed_ms, events)

    def _update(self, elapsed_ms: int, events: list):
        """
        Lifecycle method, called automatically each game tick.
        Can optionally be overridden.
        Complete any miscellaneous work necessary for this object each tick
        that is not covered by other lifecycle methods here
        """

        pass

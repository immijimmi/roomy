from recurfaces import Recurface
from objectextensions import Extendable
from pygame import Surface

from abc import ABC
from typing import Tuple, Optional, Sequence, Any


class Entity(Extendable, Recurface, ABC):
    """
    An Entity is any object that has a place in the rendering hierarchy.
    """

    def __init__(self, game, surface: Surface = None, position: Optional[Sequence[int]] = None, priority: Any = None):
        Extendable.__init__(self)
        Recurface.__init__(self, surface=surface, position=position, priority=priority)

        self._game = game

    @property
    def game(self):
        return self._game

    def update(self, elapsed_ms: int, events: Tuple):
        self._update(elapsed_ms, events)

        child: Entity
        for child in self.child_recurfaces:
            child.update(elapsed_ms, events)

    def _update(self, elapsed_ms: int, events: Tuple):
        """
        This is an overridable lifecycle method which will be called automatically in the game loop
        """

        pass

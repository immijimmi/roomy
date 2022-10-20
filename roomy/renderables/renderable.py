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
            render_position: Optional[Tuple[int, int]] = None, priority: Any = None
    ):
        Extendable.__init__(self)
        Recurface.__init__(self, surface=surface, parent=parent, position=render_position, priority=priority)

        self._game = game

    @property
    def game(self):
        return self._game

    def update(self, elapsed_ms: int, input_events: list, *args, **kwargs) -> None:
        """
        Lifecycle method, called automatically each game tick.

        *args and **kwargs can optionally be passed any additional information regarding the game tick itself;
        for example, a game which wants to prioritise updating the environment first and update the characters second
        in each loop may then choose to run at 2 updates per frame so that the game's screen can first call .update()
        with the kwarg `type="environment"` and second call .update() with the kwarg `type="characters"`.

        Note that additional *args and **kwargs can be introduced at an arbitrary point in the Renderable hierarchy, and
        do not have to be passed in starting from the game's screen object. They also do not have to be propagated
        further down the hierarchy than is necessary
        """

        self._update(elapsed_ms, input_events, *args, **kwargs)

        try:
            # Events passed to high render_priority children first, if possible
            child_recurfaces = reversed(self.ordered_child_recurfaces)
        except TypeError:
            child_recurfaces = self.child_recurfaces

        child: Renderable
        for child in child_recurfaces:
            child.update(elapsed_ms, input_events, *args, **kwargs)

    def _update(self, elapsed_ms: int, input_events: list, *args, **kwargs) -> None:
        """
        Lifecycle method, called automatically each game tick.
        Can optionally be overridden.

        Complete any miscellaneous work necessary for this object each tick
        that is not covered by other lifecycle methods here
        """

        pass

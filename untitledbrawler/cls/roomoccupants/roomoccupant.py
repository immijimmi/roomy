from typing import Sequence
from abc import ABC

from ..entity import Entity


class RoomOccupant(Entity, ABC):
    """
    Represents a persisting entity in a room.
    This includes people, inanimate objects, decorative objects, objects with no collision etc.
    Examples of excluded classes would be projectiles and hitboxes since these will not persist if the room is exited
    and will not be saved to the game state
    """

    def __init__(self, parent: Entity, render_position: Sequence[int], surface=None, priority=None):
        super().__init__(
            parent.game, parent.state, parent=parent, surface=surface, position=render_position, priority=priority
        )

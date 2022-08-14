from typing import Tuple
from abc import ABC

from ..entity import Entity


class RoomOccupant(Entity, ABC):
    """
    Concrete class tightly coupled to the Room class, which renders a persisting entity in a room.

    This includes people, inanimate objects, decorative objects, objects with no collision etc. and only
    excludes things that would cease to exist once the room is exited
    """

    def __init__(self, parent: "Room", render_position: Tuple[int, int], surface=None, priority=None):
        super().__init__(
            parent.game, parent=parent, surface=surface, position=render_position, priority=priority
        )

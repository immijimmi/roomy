from typing import Tuple
from abc import ABC

from ..stats import Stat, GenericStat
from .renderable import Renderable


class Entity(Renderable, ABC):
    """
    Concrete class tightly coupled to the Room class, which renders a persisting Renderable object in a room.

    This includes people, inanimate objects, decorative objects, objects with no collision etc. and only
    excludes things that would cease to exist once the room is exited
    """

    def __init__(self, parent: "Room", render_position: Tuple[int, int], surface=None, priority=None):
        super().__init__(
            parent.game, parent=parent, surface=surface, render_position=render_position, priority=priority
        )

    @property
    def speed(self) -> Tuple[GenericStat, GenericStat]:
        """
        Should return a pair of stat objects representing x speed and y speed, respectively.

        These stats must be concrete GenericStat objects, to expose a clear write-access interface to any external
        forces
        """

        raise NotImplementedError

    @property
    def acceleration(self) -> Tuple[GenericStat, GenericStat]:
        """
        Should return a pair of stat objects representing x acceleration and y acceleration, respectively.

        These stats must be concrete GenericStat objects, to expose a clear write-access interface to any external
        forces
        """

        raise NotImplementedError

    @property
    def mass(self) -> Stat:
        """
        Used to apply changes in momentum rather than just speed;
        For example, in a collision between two objects there may be a transfer of momentum - the speed
        of one object would be multiplied by its mass, and then divided by the other object's mass before
        being added to that other object's speed
        """

        raise NotImplementedError

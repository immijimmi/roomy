from typing import Tuple, Iterable


class Coords:
    def __init__(self, x: int, y: int):
        self._full = [x, y]

    @property
    def full(self) -> Tuple[int, ...]:
        return tuple(self._full)

    @full.setter
    def full(self, value: Iterable[int]):
        value = list(value)
        assert len(value) == 2

        self._full = value

    @property
    def x(self) -> int:
        return self._full[0]

    @x.setter
    def x(self, value: int):
        self._full[0] = value

    @property
    def y(self) -> int:
        return self._full[1]

    @y.setter
    def y(self, value: int):
        self._full[1] = value

    def __add__(self, other: "Coords"):
        assert isinstance(other, Coords)

        return Coords(self.x + other.x, self.y + other.y)


class CoordsVector(Coords):
    """
    This class is only used to distinguish when a coords object is not a reference to a location
    and is instead a vector intended to be added to another set of coords.
    """
    pass

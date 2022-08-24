from abc import ABC
from functools import total_ordering
from operator import add, sub, mul, truediv, floordiv, mod
from typing import Callable, Tuple


@total_ordering
class Stat(ABC):
    @property
    def total(self) -> float:
        raise NotImplementedError

    def __str__(self):
        return str(self.total)

    # Note that @total_ordering covers the comparison methods that are not implemented here
    def __lt__(self, other):
        if issubclass(type(other), Stat):
            return self.total < other.total

        else:
            return self.total < other

    def __eq__(self, other):
        if issubclass(type(other), Stat):
            return self.total == other.total

        else:
            return self.total == other

    def __add__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), add)

    def __sub__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), sub)

    def __mul__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), mul)

    def __truediv__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), truediv)

    def __floordiv__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), floordiv)

    def __mod__(self, other):
        if not issubclass(type(other), Stat):
            return NotImplemented

        return CombinedStat((self, other), mod)


class CombinedStat(Stat):
    """
    Represents the result of applying an arithmetic operation on two other stat objects.
    Stores live references to its constituent stat objects so that it may update accordingly when either one changes.

    Each time this stat's total value is calculated, the two constituent stat objects' current values are
    passed (in order) into the provided operator function, and the result is returned.

    These constituent stat objects can also be CombinedStat objects, allowing complex equations to be modeled using
    chains of CombinedStat objects to reach the desired result
    """

    def __init__(self, operands: Tuple[Stat, Stat], operator: Callable[[float, float], float]):
        self._operands = tuple(operands)
        self._operator = operator  # Can be a basic arithmetic operator function, or a custom algorithm as needed

        self._subtotals = (None, None)  # Will be calculated as needed
        self._total = None  # Will be calculated as needed

    @property
    def operands(self) -> Tuple[Stat, Stat]:
        return self._operands

    @property
    def total(self) -> float:
        # Pulling fresh subtotals from the referenced stat objects
        subtotals = (self._operands[0].total, self._operands[1].total)

        # Checking if the total needs recalculating
        # (either the current total is None, or the fresh subtotals don't match the stored ones)
        if (subtotals == self._subtotals) and self._total is not None:  # Does not need recalculating
            return self._total

        else:
            self._subtotals = subtotals

            self._total = self._operator(*subtotals)
            return self._total

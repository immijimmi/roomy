from typing import FrozenSet, Hashable, Any
from contextlib import contextmanager

from .methods import ErrorMessages
from .stat import Stat


class GenericStat(Stat):
    """
    This class provides a standardised interface for any generic stat, which aims to facilitate the kinds of changes
    and modifiers typically applied to stats via game mechanics.

    It is made up of three main segments - a base value, an added secondary value, and an overall multiplier.
    This can be further broken down:
    - The base and secondary values have two individual multipliers *each*, which are applied to them
      before they are then added together
    - The overall multiplier is also comprised of two individual multipliers, which are both applied
      after the base and secondary values have been added together

    The reason for this structure is that each segment of the formula has one multiplier comprised from
    addition operations, and one multiplier comprised from multiplication operations. This separation in multipliers
    means that order of operations does not matter, so changes to these values may be applied and later reverted freely
    without leaving a permanent effect on the total value.

    Each of these factors is named with clarity for the player in mind - it makes intuitive sense that "base damage"
    and "secondary damage" would be added together when calculating the total, for example.

    If this stat is currently locked (self.is_locked is True or truthy), any attempted changes to these factors
    will raise an exception. Thus, it is important to check this attribute before making any changes,
    and unlock the stat if necessary.

    In practice, each of these attributes should be used as shown below:
    damage = GenericStat()

    # Apply double damage (x2 multiplier)
    damage.overall_multiplied_modifier *= 2
    # Remove double damage
    damage.overall_multiplied_modifier /= 2

    # Apply 10% increased damage
    damage.overall_summed_modifier += 0.1

    # Apply double secondary damage (x2 multiplier)
    damage.secondary_multiplied_modifier *= 2

    # Apply 10% increased secondary damage
    damage.secondary_summed_modifier += 0.1

    # Apply +2 secondary damage
    damage.secondary_value += 2

    # Apply double base damage (x2 multiplier)
    damage.base_multiplied_modifier *= 2

    # Apply 10% increased base damage
    damage.base_summed_modifier += 0.1

    # Apply +2 base damage
    damage.base_value += 2
    """

    def __init__(
            self,
            base_value: float = 0, base_summed_modifier: float = 1, base_multiplied_modifier: float = 1,
            secondary_value: float = 0, secondary_summed_modifier: float = 1, secondary_multiplied_modifier: float = 1,
            overall_summed_modifier: float = 1, overall_multiplied_modifier: float = 1,
            is_locked: Any = False
    ):
        self._base_value = base_value
        self._base_summed_modifier = base_summed_modifier
        self._base_multiplied_modifier = base_multiplied_modifier

        self._secondary_value = secondary_value
        self._secondary_summed_modifier = secondary_summed_modifier
        self._secondary_multiplied_modifier = secondary_multiplied_modifier

        self._overall_summed_modifier = overall_summed_modifier
        self._overall_multiplied_modifier = overall_multiplied_modifier

        self._is_locked = is_locked

        self._total = None  # Will be calculated as needed

        self._modified_by = set()
        self._modified_by_frozen = None  # Will be calculated as needed

    def __repr__(self):
        return (
            f"<{type(self).__name__}(base_value={self._base_value}, base_summed_modifier={self._base_summed_modifier}, "
            f"base_multiplied_modifier={self._base_multiplied_modifier}, secondary_value={self._secondary_value}, "
            f"secondary_summed_modifier={self._secondary_summed_modifier}, "
            f"secondary_multiplied_modifier={self._secondary_multiplied_modifier}, "
            f"overall_summed_modifier={self._overall_summed_modifier}, "
            f"overall_multiplied_modifier={self._overall_multiplied_modifier}, is_locked={self._is_locked}) "
            f"modified by {repr(self._modified_by)}>"
        )

    @property
    def base_value(self) -> float:
        return self._base_value

    @base_value.setter
    def base_value(self, value: float):
        """
        This attribute should only have *additions* and *subtractions* applied to it,
        **not** multiplications or divisions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._base_value:
            return

        self._base_value = value
        self._total = None

    @property
    def base_summed_modifier(self) -> float:
        return self._base_summed_modifier

    @base_summed_modifier.setter
    def base_summed_modifier(self, value: float):
        """
        This attribute should only have *additions* and *subtractions* applied to it,
        **not** multiplications or divisions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._base_summed_modifier:
            return

        self._base_summed_modifier = value
        self._total = None

    @property
    def base_multiplied_modifier(self) -> float:
        return self._base_multiplied_modifier

    @base_multiplied_modifier.setter
    def base_multiplied_modifier(self, value: float):
        """
        This attribute should only have *multiplications* and *divisions* applied to it,
        **not** additions or subtractions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._base_multiplied_modifier:
            return

        self._base_multiplied_modifier = value
        self._total = None

    @property
    def secondary_value(self) -> float:
        return self._secondary_value

    @secondary_value.setter
    def secondary_value(self, value: float):
        """
        This attribute should only have *additions* and *subtractions* applied to it,
        **not** multiplications or divisions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._secondary_value:
            return

        self._secondary_value = value
        self._total = None

    @property
    def secondary_summed_modifier(self) -> float:
        return self._secondary_summed_modifier

    @secondary_summed_modifier.setter
    def secondary_summed_modifier(self, value: float):
        """
        This attribute should only have *additions* and *subtractions* applied to it,
        **not** multiplications or divisions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._secondary_summed_modifier:
            return

        self._secondary_summed_modifier = value
        self._total = None

    @property
    def secondary_multiplied_modifier(self) -> float:
        return self._secondary_multiplied_modifier

    @secondary_multiplied_modifier.setter
    def secondary_multiplied_modifier(self, value: float):
        """
        This attribute should only have *multiplications* and *divisions* applied to it,
        **not** additions or subtractions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._secondary_multiplied_modifier:
            return

        self._secondary_multiplied_modifier = value
        self._total = None

    @property
    def overall_summed_modifier(self) -> float:
        return self._overall_summed_modifier

    @overall_summed_modifier.setter
    def overall_summed_modifier(self, value: float):
        """
        This attribute should only have *additions* and *subtractions* applied to it,
        **not** multiplications or divisions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._overall_summed_modifier:
            return

        self._overall_summed_modifier = value
        self._total = None

    @property
    def overall_multiplied_modifier(self) -> float:
        return self._overall_multiplied_modifier

    @overall_multiplied_modifier.setter
    def overall_multiplied_modifier(self, value: float):
        """
        This attribute should only have *multiplications* and *divisions* applied to it,
        **not** additions or subtractions
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if value == self._overall_multiplied_modifier:
            return

        self._overall_multiplied_modifier = value
        self._total = None

    @property
    def is_locked(self) -> Any:
        """
        Determines whether the other attributes of this instance may be modified
        (effectively whether this stat instance is currently mutable or not)

        The value can either be set to True/False to function as a simple *is locked*/*is not locked* flag,
        or can instead be set to a permission level (e.g. using an enum for standardised permissions values)
        which should be matched by any client code that wishes to modify or unlock this stat instance
        """

        return self._is_locked

    @is_locked.setter
    def is_locked(self, value: Any):
        """
        Any source that is setting a value to this property should check first that it supercedes the
        permission level stored in the current value of .is_locked (if its value is not simply True)
        """

        self._is_locked = value

    @property
    def total(self) -> float:
        if self._total is None:
            self._total = (
                (
                    (self._base_value * self._base_summed_modifier * self._base_multiplied_modifier)
                    + (self._secondary_value * self._secondary_summed_modifier * self._secondary_multiplied_modifier)
                )
                * self._overall_summed_modifier * self._overall_multiplied_modifier
            )

        return self._total

    @property
    def modified_by(self) -> FrozenSet[Hashable]:
        if self._modified_by_frozen is None:
            self._modified_by_frozen = frozenset(self._modified_by)

        return self._modified_by_frozen

    def add_modified_by(self, identifier: Hashable) -> None:
        """
        Optional.
        Allows a source to register that it has modified this stat.
        This functionality allows a source to later check if a previous modification it wishes to revert was actually
        applied, or was prevented due to the stat being locked at the time, without needing to store this information
        itself.

        The identifier provided should be unique to the specific instance of modification taking place, as collisions
        with other instances of modification may cause unintended behaviour
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if identifier in self._modified_by:
            return

        self._modified_by.add(identifier)
        self._modified_by_frozen = None

    def remove_modified_by(self, identifier: Hashable) -> None:
        """
        Optional.
        Allows a source to register that it has reverted a modification to this stat.

        This is the inverse of .add_modified_by(), and so the same stipulations apply
        """

        if self._is_locked:
            ErrorMessages.stat_locked()
        if identifier not in self._modified_by:
            return

        self._modified_by.remove(identifier)
        self._modified_by_frozen = None

    @contextmanager
    def unlocked(self, permission_level: Any):
        """
        Temporarily unlocks this stat instance to allow modifications to be made, then replaces the lock value as it
        was before unlocking. Requires a value greater than or equal to .is_locked to be given via `permission_level`;
        If this requirement is not met, an exception will be raised
        """

        if permission_level < self._is_locked:
            raise PermissionError(f"insufficient permissions to unlock object: {permission_level} < {self._is_locked}")

        is_locked_value = self._is_locked

        self._is_locked = False
        yield
        self._is_locked = is_locked_value

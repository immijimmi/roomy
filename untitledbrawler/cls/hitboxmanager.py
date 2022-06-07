from typing import Set, FrozenSet, Optional, Callable, Iterable, Hashable, Union
from weakref import ref

from .hitboxes import Hitbox


class HitboxManager:
    def __init__(self, screen: "Screen"):
        self._screen = ref(screen)  # Weakref so that it does not prevent parent object being garbage collected

        self._hitboxes = set()
        self._hitboxes_by_tag = {}

        self._checked_collisions = set()

    @property
    def screen(self) -> "Screen":
        return self._screen()

    @property
    def checked_collisions(self) -> Set[FrozenSet[Union[Hitbox, "Entity.with_extensions(Hitboxed)"]]]:
        """
        This set represents every unique hitbox combination that has already been checked for a collision in this tick.
        Each combination is stored here as a frozenset containing the involved hitbox instances
        """

        return self._checked_collisions

    def add(self, hitbox: Hitbox) -> None:
        for tag in hitbox.tags:
            if tag not in self._hitboxes_by_tag:
                self._hitboxes_by_tag[tag] = set()

            self._hitboxes_by_tag[tag].add(hitbox)

        self._hitboxes.add(hitbox)

    def remove(self, hitbox: Hitbox) -> None:
        for tag in hitbox.tags:
            self._hitboxes_by_tag[tag].remove(hitbox)

        self._hitboxes.remove(hitbox)

    def get(
            self,
            tags_any: Optional[Iterable[Hashable]] = None, tags_all: Optional[Iterable[Hashable]] = None,
            custom_filter_key: Optional[Callable] = None
    ) -> FrozenSet[Hitbox]:
        """
        This is a querying method to retrieve a subsection of hitboxes in order to optimise collision checking.
        tags_any defines tags of which at least one must to be present in each returned hitbox, tags_all defines tags
        of which all must be present in each returned hitbox and custom_filter_key will be used to further narrow
        down the results as a more specific filter key.

        If None is provided for each of these parameters, they are simply not used to filter hitboxes down.
        Therefore, providing None for all parameters will result in every hitbox being returned
        """

        if tags_any is None:
            result = set(self._hitboxes)
        else:
            result = set()

            for tag_to_include in tags_any:
                for hitbox_with_tag_to_include in self._hitboxes_by_tag[tag_to_include]:
                    result.add(hitbox_with_tag_to_include)

        if tags_all is None:
            pass
        else:
            hitbox_has_required_tags = lambda hitbox: all(
                required_tag in hitbox.tags for required_tag in tags_all
            )
            result = filter(hitbox_has_required_tags, result)

        if custom_filter_key is not None:
            result = frozenset(filter(custom_filter_key, result))
        else:
            result = frozenset(result)

        return result

    def reset_checked_collisions(self) -> None:
        self._checked_collisions = set()

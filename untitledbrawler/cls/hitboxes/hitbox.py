from typing import Iterable, Hashable, Optional, FrozenSet
from abc import ABC
from weakref import ref

from ..entity import Entity


class Hitbox(ABC):
    def __init__(self, tags: Iterable[Hashable], parent: Optional["Entity.with_extensions(Hitboxed)"] = None):
        self._tags: FrozenSet[Hashable] = frozenset(tags)

        # Weakref so that it does not prevent parent object being garbage collected
        self._parent = lambda: None if parent is None else ref(parent)

    @property
    def tags(self) -> FrozenSet[Hashable]:
        return self._tags

    @property
    def parent(self) -> "Entity.with_extensions(Hitboxed)":
        return self._parent()

    def is_collision(self, other: "Hitbox") -> bool:
        raise NotImplementedError

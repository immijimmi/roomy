from abc import ABC
from typing import Iterable, FrozenSet


class Tagged(ABC):
    def __init__(self, tags: Iterable[str]):
        for tag in tags:
            if not self._is_valid_tag(tag):
                raise ValueError(f"Invalid tag provided: {tag}")

        self._tags: FrozenSet[str] = frozenset(tags)

    @property
    def tags(self) -> FrozenSet[str]:
        return self._tags

    def _is_valid_tag(self, tag: str) -> bool:
        """
        Must be overridden.
        Should check whether the provided tag is a valid tag for this object's class
        """

        raise NotImplementedError

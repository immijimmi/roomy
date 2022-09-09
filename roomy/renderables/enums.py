from enum import Enum


class EntityDataKey(str, Enum):
    CLASS = "class"

    ARGS = "args"
    KWARGS = "kwargs"

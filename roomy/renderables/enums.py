from enum import Enum


class OccupantDataKey(str, Enum):
    CLASS = "class"

    ARGS = "args"
    KWARGS = "kwargs"

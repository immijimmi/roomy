from enum import Enum


class RenderableHitboxTag(str, Enum):
    ROOM = "room"

    ROOM_OCCUPANT = "room_occupant"


class RoomOccupantDataKey(str, Enum):
    CLASS = "class"

    ARGS = "args"
    KWARGS = "kwargs"

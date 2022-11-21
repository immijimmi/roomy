from enum import Enum


class RenderableHitboxTag(str, Enum):
    ROOM = "room"

    ROOM_OCCUPANT = "room_occupant"


class StateRenderableDataKey(str, Enum):
    CLASS = "class"

    ARGS = "args"  # Refers to any custom positional args that should be passed into the constructor for a Renderable
    KWARGS = "kwargs"  # Refers to any custom keyword args that should be passed into the constructor for a Renderable

from enum import Enum


class RenderableDataKey(str, Enum):
    """
    Standardised keys to access Renderable object data stored in an instance of the World class
    """

    CLASS = "class"

    ARGS = "args"  # Refers to any custom positional args that should be passed into the constructor for a Renderable
    KWARGS = "kwargs"  # Refers to any custom keyword args that should be passed into the constructor for a Renderable

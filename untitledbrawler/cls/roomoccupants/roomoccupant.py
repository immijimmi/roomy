from ..entity import Entity


class RoomOccupant(Entity):
    """
    Represents a persisting entity in a room.
    This includes people, inanimate objects, decorative objects, objects with no collision etc.
    Examples of excluded classes would be projectiles and hitboxes since these will not persist if the room is exited
    and will not be saved to the game state
    """

    pass  ##### TODO

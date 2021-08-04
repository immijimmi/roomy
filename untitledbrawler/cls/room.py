from .entity import Entity
from .ext import Animated


class Room(Entity.with_extensions(Animated)):
    def __init__(self, world: "World"):
        super().__init__(position=(0, 0))

        self.parent = world

        ##### TODO

    def _update(self, elapsed_ms, events):
        pass

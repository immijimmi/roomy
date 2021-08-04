from pygame import Surface

from abc import ABC

from ..entity import Entity


class Screen(Entity, ABC):
    """
    A class that implements Screen is a top-level object in the game loop.
    Any objects to be rendered to the display should be nested under this in its .children property.
    Different derived classes of Screen should represent different views of the game;
    for example, the start menu would be one Screen class whereas the game world would be a separate Screen class
    """

    def __init__(self, game: "Game"):
        self._game = game

        # Screen objects are only containers for child entities so as a recurface they simply render a black rectangle
        surface = Surface((game.window.get_width(), game.window.get_height()))
        surface.fill((0, 0, 0))
        position = (0, 0)

        super().__init__(surface, position)

    @property
    def game(self) -> "Game":
        return self._game

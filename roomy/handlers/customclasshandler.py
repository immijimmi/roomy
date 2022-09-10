from sys import modules
from typing import Dict


class CustomClassHandler:
    def __init__(self, game):
        self._game = game

        self._classes = {**self._game.config.CUSTOM_CLASSES}

    def update(self, value: Dict[str, type]) -> None:
        self._classes.update(value)

    def get(self, class_name: str) -> type:
        """
        Attempts to locate a class using the provided class name.
        First checks locally stored classes (initially populated from Config.CUSTOM_CLASSES
        but additional classes can be manually added during runtime),
        then checks classes in the global namespace (in __main__).
        Supports dot notation to access objects stored under module or class attributes in the global namespace
        """

        if class_name in self._classes:
            return self._classes[class_name]

        try:
            nodes = class_name.split(".")

            result = getattr(modules["__main__"], nodes.pop(0))
            for node in nodes:
                result = getattr(result, node)

            return result

        except AttributeError:
            raise ValueError(f"unable to resolve the class name '{class_name}'")

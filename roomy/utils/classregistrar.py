from sys import modules
from logging import warning


class ClassRegistrar:
    """
    Makes provided custom classes available to tools in this library which must
    dynamically populate their components from plaintext schematics
    """

    def __init__(self, game):
        self._game = game

        self._classes = {**self._game.config.CUSTOM_CLASSES}
        self._search_global = self._game.config.ALLOW_GLOBAL_CUSTOM_CLASSES

    def register(self, **classes: type) -> None:
        """
        Stores the provided classes under their associated provided names, to be retrieved as needed later.
        This method will output a warning message if stored classes are overwritten, but will not prevent
        them from being overwritten
        """

        for cls_key, cls in classes.items():
            if (cls_key in self._classes) and (self._classes[cls_key] != cls):
                warning(
                    f"{type(self).__name__} has had an entry in its registry overwritten:"
                    f" '{cls_key}' now refers to {cls.__name__} instead of {self._classes[cls_key].__name__}"
                )

        self._classes.update(classes)

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

        if self._search_global:
            try:
                nodes = class_name.split(".")

                result = getattr(modules["__main__"], nodes.pop(0))
                for node in nodes:
                    result = getattr(result, node)

                return result

            except AttributeError:
                pass

        raise ValueError(f"unable to resolve the class name '{class_name}'")

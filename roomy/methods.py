from sys import modules
from typing import Dict, Any


class Methods:
    CLASSES = {}

    @staticmethod
    def get_class_attrs(target_cls: type) -> Dict[str, Any]:
        """
        Returns a dict of {name: value}, containing all attributes bound to a class
        """

        return {k: v for k, v in vars(target_cls).items() if not k.startswith("__")}

    @staticmethod
    def get_object_from_str(object_name: str):
        """
        Returns the value stored under the provided name, in the global namespace
        """

        return getattr(modules["__main__"], object_name)

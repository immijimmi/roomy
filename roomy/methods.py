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
    def get_obj_by_str_name(object_name: str):
        """
        Returns the value stored under the provided name, in the global namespace.
        Supports dot notation to access objects stored under module or class attributes
        """

        nodes = object_name.split(".")

        obj = getattr(modules["__main__"], nodes.pop(0))
        for node in nodes:
            obj = getattr(obj, node)

        return obj


class ErrorMessages:
    @staticmethod
    def stat_locked():
        raise PermissionError("cannot modify this object while .is_locked is set to a truthy value")

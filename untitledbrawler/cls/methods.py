from sys import modules
from typing import Dict, Any


class Methods:
    CLASSES = {}

    @staticmethod
    def get_class_attrs(cls) -> Dict[str, Any]:
        return {k: v for k, v in vars(cls).items() if not k.startswith("__")}

    @staticmethod
    def get_class_from_str(class_name: str):
        Methods._load_class(class_name)

        return Methods.CLASSES[class_name]

    @staticmethod
    def _load_class(class_name: str):
        if class_name in Methods.CLASSES:
            return

        for module_name in modules:
            if "cls." in module_name:
                module = modules[module_name]

                try:
                    Methods.CLASSES[class_name] = getattr(module, class_name)
                except AttributeError:
                    pass

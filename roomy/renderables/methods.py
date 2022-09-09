from sys import modules


class Methods:
    # Allows manual caching of objects for .get_obj_by_str_name() that may not be available in the global namespace
    REGISTERED_OBJECTS = {}

    @staticmethod
    def get_obj_by_str_name(object_name: str):
        """
        Returns the value stored under the provided name, in the global namespace (in __main__).
        Supports dot notation to access objects stored under module or class attributes
        """

        try:
            nodes = object_name.split(".")

            obj = getattr(modules["__main__"], nodes.pop(0))
            for node in nodes:
                obj = getattr(obj, node)

            return obj

        except AttributeError:
            if object_name in Methods.REGISTERED_OBJECTS:
                return Methods.REGISTERED_OBJECTS[object_name]

            else:
                raise ValueError(f"unable to locate an object in the global namespace with the name '{object_name}'")

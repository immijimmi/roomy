from sys import modules


class Methods:
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

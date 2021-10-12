from sys import modules


class Methods:
    @staticmethod
    def get_class_from_str(class_module: str, class_name: str):
        """
        class_module is in the format: 'game.cls.classfilename' where game and cls are directory names
        """

        return getattr(modules[class_module], class_name)

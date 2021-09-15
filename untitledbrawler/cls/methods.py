import sys


class Methods:
    @staticmethod
    def get_class_from_str(class_name: str):
        return getattr(sys.modules[__name__], class_name)

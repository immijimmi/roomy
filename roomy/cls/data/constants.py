from managedstate.extensions import PartialQuery


class Constants:
    PATH_DYNAMIC_KEY = PartialQuery(lambda key: key)

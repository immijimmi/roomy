from pygame import Surface, image

from json import loads
from typing import Type, Dict, Any


class AnimationHandler:
    """
    Helper class which retrieves and stores animation data
    """

    # For performance optimisation. Stores data which has already been loaded before using file paths as their keys
    data = {}
    # For performance optimisation, stores frames which have already been generated using file paths as their keys
    frames = {}

    @staticmethod
    def get_data(target_cls: Type["Entity.with_extensions(Animated)"], animation_key: str) -> Dict[str, Any]:
        AnimationHandler._load_data(target_cls)

        return AnimationHandler.data[target_cls.__name__][animation_key]

    @staticmethod
    def get_frame(file_path: str) -> Surface:
        AnimationHandler._load_frame(file_path)

        return AnimationHandler.frames[file_path]

    @staticmethod
    def _load_data(target_cls: Type["Entity.with_extensions(Animated)"]) -> None:
        """
        Loads all animation data for the target class, if it is not already loaded
        """

        if target_cls.__name__ not in AnimationHandler.data:
            animation_data_file_path = rf"untitledbrawler\res\{target_cls.__name__}\animation_data.json"

            with open(animation_data_file_path, "r") as file:
                data = loads(file.read())
                AnimationHandler.data[target_cls.__name__] = data

    @staticmethod
    def _load_frame(file_path: str) -> None:
        """
        Loads the animation frame at the target file path, if it is not already loaded
        """

        if file_path not in AnimationHandler.frames:
            AnimationHandler.frames[file_path] = image.load(file_path).convert_alpha()

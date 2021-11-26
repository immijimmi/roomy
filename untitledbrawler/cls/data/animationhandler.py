from pygame import Surface, image, transform

from json import loads
from typing import Type, Dict, Any


class AnimationHandler:
    """
    Helper class which retrieves and stores animation data
    """

    # For performance optimisation. Stores data which has already been loaded before, using file paths as their keys
    DATA = {}
    # For performance optimisation. Stores frames which have already been generated, using file paths as their keys
    FRAMES = {}

    @staticmethod
    def get_data(target_cls: Type["Entity.with_extensions(Animated)"], animation_key: str) -> Dict[str, Any]:
        AnimationHandler._load_data(target_cls)

        return AnimationHandler.DATA[target_cls.__name__][animation_key]

    @staticmethod
    def get_frame(file_path: str, size: float = 1) -> Surface:
        AnimationHandler._load_frame(file_path, size)

        return AnimationHandler.FRAMES[file_path][size]

    @staticmethod
    def _load_data(target_cls: Type["Entity.with_extensions(Animated)"]) -> None:
        """
        Loads all animation data for the target class, if it is not already loaded.

        The animation data that is retrieved via this method includes any parameters that have the possibility of being
        unique to an animation - typically this includes the animation's frames, default framerate etc. - since
        these unique parameters are the ones that it is worth abstracting into a data file, rather than keeping them
        directly integrated in a class.

        The structure of data in each file (containing all animation data for one `Animated` class)
        is expected to be as follows:
        {
            "<animation key>": {
                "<animation parameter key>": <value>,
                "<another animation parameter key>": <value>,
                ...
            },
            "<another animation key>": {
            ...
            }
            ...
        }
        """

        if target_cls.__name__ not in AnimationHandler.DATA:
            animation_data_file_path = rf"untitledbrawler\res\{target_cls.__name__}\animation_data.json"

            with open(animation_data_file_path, "r") as file:
                data = loads(file.read())
                AnimationHandler.DATA[target_cls.__name__] = data

    @staticmethod
    def _load_frame(file_path: str, size: float) -> None:
        """
        Loads the animation frame at the target file path and size, if it is not already loaded.
        """

        if file_path not in AnimationHandler.FRAMES or size not in AnimationHandler.FRAMES[file_path]:
            frame_sizes = AnimationHandler.FRAMES.get(file_path, {})

            surface = image.load(file_path).convert_alpha()
            surface = transform.rotozoom(surface, 0, size)
            frame_sizes[size] = surface

            AnimationHandler.FRAMES[file_path] = frame_sizes

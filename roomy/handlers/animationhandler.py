from pygame import Surface, image, transform

from os import path
from json import loads
from typing import Type, Dict, Any, Tuple, Union, Literal

from ..constants import Constants as GameConstants
from .enums import AnimationDataKey


class AnimationHandler:
    """
    Helper class which retrieves and stores animation data
    """

    # For performance optimisation. Stores animation data which has already been loaded before, by (Animated) class name
    ANIMATION_DATA = {}
    # Stores data for any sprite sheets loaded as part of animation data, under the sprite sheet's label
    SPRITE_SHEETS_DATA = {}

    # For performance optimisation. Stores frames which have already been generated, under their frame key & size
    FRAMES = {}

    @staticmethod
    def register_sprite_sheet(
        sprite_label: str,
        sprite_data: Dict[
            Literal[AnimationDataKey.FILE_PATH, AnimationDataKey.PARSE_TYPE, AnimationDataKey.PARSE_DATA], Any
        ]
    ) -> None:
        """
        Stores data relating to a sprite sheet, to enable the relevant sprites to be loaded later if necessary
        """

        AnimationHandler.SPRITE_SHEETS_DATA[sprite_label] = sprite_data

    @staticmethod
    def get_settings(target_cls: Type["Renderable.with_extensions(Animated)"], animation_key: str) -> Dict[str, Any]:
        """
        Retrieves the animation settings associated with the provided class and animation key,
        loading the class's animation data if necessary
        """

        AnimationHandler._load_data(target_cls)

        class_animation_data = AnimationHandler.ANIMATION_DATA[target_cls.__name__]
        class_animation_settings = class_animation_data[AnimationDataKey.ANIMATION_SETTINGS]
        return class_animation_settings[animation_key]

    @staticmethod
    def get_frame(frame_key: Union[str, Tuple[str, int]], size: float = 1) -> Surface:
        """
        Retrieves an animation frame using the provided frame key and size modifier, loading the frame if necessary
        """

        AnimationHandler._load_frame(frame_key, size)

        return AnimationHandler.FRAMES[frame_key][size]

    @staticmethod
    def _load_data(target_cls: Type["Renderable.with_extensions(Animated)"]) -> None:
        """
        Loads all animation data for the target class, if it is not already loaded.
        Assumes a standard location for the data file as dictated below in the variable `animation_data_file_path`.

        The animation data that is retrieved via this method should include any custom parameters that pertain *only*
        to the animation itself (as opposed to the use case you are implementing it in);
        typically this can include the animation's frames, default framerate etc.

        Sprite sheets are considered unique by label for the purposes of this handler class, meaning that if the same
        sprite sheet label appears in multiple data files, its associated data should be identical.
        To avoid duplication issues resulting from this arrangement, it is recommended to minimise the amount of
        sprite sheets being defined in animation data files, and instead call .register_sprite_sheet() manually
        in your Animated class' constructors (or elsewhere) as necessary
        """

        if target_cls.__name__ not in AnimationHandler.ANIMATION_DATA:
            animation_data_file_path = path.join(
                GameConstants.RESOURCE_FOLDER_PATH,
                f"{target_cls.__name__}",
                "animation_data.json"
            )

            with open(animation_data_file_path, "r") as file:
                data = loads(file.read())
                sprite_sheets_data = data.get(AnimationDataKey.SPRITE_SHEETS, {})

                AnimationHandler.ANIMATION_DATA[target_cls.__name__] = data
                AnimationHandler.SPRITE_SHEETS_DATA.update(sprite_sheets_data)

    @staticmethod
    def _load_frame(frame_key: Union[str, Tuple[str, int]], size: float) -> None:
        """
        Loads the animation frame at the target size modifier, if it is not already loaded.
        """

        if frame_key not in AnimationHandler.FRAMES or size not in AnimationHandler.FRAMES[frame_key]:
            if type(frame_key) is str:  # frame_key is a file path
                surface = image.load(frame_key).convert_alpha()
                surface = transform.rotozoom(surface, 0, size)

                frame_sizes = AnimationHandler.FRAMES.setdefault(frame_key, {})
                frame_sizes[size] = surface

            else:  # frame_key is a sprite sheet label
                sprite_label = frame_key[0]
                sprite_index = frame_key[1]

                sprite_sheet_data = AnimationHandler.SPRITE_SHEETS_DATA[sprite_label]
                pass  ##### TODO: Add logic to load & store sprites from sprite sheet data at provided zoom

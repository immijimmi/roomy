from pygame import Surface, transform

from os import path
from json import loads
from typing import Type, Dict, Any, Tuple, Union, Literal

from ..methods import Methods
from .enums import AnimationDataKey


class AnimationHandler:
    """
    Helper class which retrieves and caches files and data for animations
    """

    def __init__(self, game):
        self._game = game

        # The below attributes cache data for performance optimisation
        # Stores animation data which has already been loaded before, by (Animated) class name
        self._animation_data = {}
        # Stores data for any sprite sheets loaded as part of animation data, under the sprite sheet's label
        self._sprite_sheets_data = {}
        # Stores frames which have already been generated, under their frame key & size
        self._frames = {}

    def register_sprite_sheet(
        self,
        sprite_sheet_label: str,
        sprite_data: Dict[
            Literal[AnimationDataKey.FILE_PATH, AnimationDataKey.PARSE_TYPE, AnimationDataKey.PARSE_DATA], Any
        ]
    ) -> None:
        """
        Stores data relating to a sprite sheet, to enable the relevant sprites to be loaded later if necessary
        """

        self._sprite_sheets_data[sprite_sheet_label] = sprite_data

    def get_settings(self, target_cls: Type["Renderable.with_extensions(Animated)"], animation_key: str) -> Dict[str, Any]:
        """
        Retrieves the animation settings associated with the provided class and animation key,
        loading the class's animation data if necessary
        """

        self._load_data(target_cls)

        class_animation_data = self._animation_data[target_cls.__name__]
        class_animation_settings = class_animation_data[AnimationDataKey.ANIMATION_SETTINGS]
        return class_animation_settings[animation_key]

    def get_frame(self, frame_key: Union[str, Tuple[str, int]], size: float = 1) -> Surface:
        """
        Retrieves an animation frame using the provided frame key and size modifier, loading the frame if necessary.

        The frame key should either be a relative path to an image file for the frame
        (relative beginning from the designated resource folder, as indicated in the game's config),
        or it should be a sequence of 2 items
        (the first a sprite sheet label which refers to an already loaded sprite sheet,
        and the second an index for which sprite within in that sprite sheet is the desired frame)
        """

        self._load_frame(frame_key, size)

        return self._frames[frame_key][size]

    def preload_frames(self, *frame_keys: Union[str, Tuple[str, int]], sizes: Tuple[int, ...] = (1,)) -> None:
        """
        Loads animation frames into memory ahead of time,
        to prevent bottlenecking when many new frames are required in a short span
        """

        for frame_key in frame_keys:
            for size in sizes:
                self._load_frame(frame_key, size)

    def _load_data(self, target_cls: Type["Renderable.with_extensions(Animated)"]) -> None:
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
        in your Animated classes' constructors (or elsewhere) as necessary
        """

        if target_cls.__name__ not in self._animation_data:
            animation_data_file_path = path.join(
                self._game.config.RESOURCE_FOLDER_PATH,
                f"{target_cls.__name__}",
                "animation_data.json"
            )

            with open(animation_data_file_path, "r") as file:
                data = loads(file.read())
                sprite_sheets_data = data.get(AnimationDataKey.SPRITE_SHEETS, {})

                self._animation_data[target_cls.__name__] = data
                self._sprite_sheets_data.update(sprite_sheets_data)

    def _load_frame(self, frame_key: Union[str, Tuple[str, int]], size: float) -> None:
        """
        Loads the animation frame at the target size modifier, if it is not already loaded.
        """

        if frame_key not in self._frames or size not in self._frames[frame_key]:
            if type(frame_key) is str:  # frame_key is a file path
                surface = Methods.load_image(
                    path.join(
                        self._game.config.RESOURCE_FOLDER_PATH,
                        frame_key
                    )
                )
                surface = transform.rotozoom(surface, 0, size)

                frame_sizes = self._frames.setdefault(frame_key, {})
                frame_sizes[size] = surface

            else:  # frame_key is a sprite sheet label
                sprite_sheet_label = frame_key[0]
                sprite_index = frame_key[1]

                sprite_sheet_data = self._sprite_sheets_data[sprite_sheet_label]
                pass  # TODO: Add logic to load & store sprites from sprite sheet data at provided zoom

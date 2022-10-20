from enum import Enum


class GameEventKey(str, Enum):
    """
    Constants representing game events which may be triggered
    via calls within this package to GameEventHandler.on_event()
    """

    UPDATE = "update"

    CHANGE_SCREEN = "change_screen"
    CHANGE_ROOM = "change_room"


class AnimationDataKey(str, Enum):
    """
    Constants representing JSON keys which are used in the files containing animation data.

    The structure of data in each file (containing all animation data for one `Animated` class)
    is expected to be as follows:
    {
        "sprite_sheets": {
            "<sprite label>": {
                "file_path": <str value>,
                "parse_type": "individual",
                "parse_data": [
                    [[<int x start>, <int y start>], [<int x end>, <int y end>]],
                    ...
                ]
            },
            ...
        },

        "animation_settings": {
            "<animation key>": {
                "frames": [
                    "<frame key>",
                    "<another frame key>",
                    ...
                ],
                "<animation parameter key>": <value>,
                "<another animation parameter key>": <value>,
                ...
            },

            "<another animation key>": {
                ...
            },
            ...
        }
    }
    """

    # Top-Level Keys
    SPRITE_SHEETS = "sprite_sheets"
    ANIMATION_SETTINGS = "animation_settings"

    # Generic
    FILE_PATH = "file_path"

    # Sprite Sheet Data
    PARSE_TYPE = "parse_type"
    PARSE_TYPE_INDIVIDUAL = "individual"
    PARSE_DATA = "parse_data"

    # Animation Settings
    FRAMES = "frames"  # Should retrieve a list of frame keys
    # Animation-specific default FPS (overrides the generic default animation FPS in the game's config)
    DEFAULT_FPS = "default_fps"  # Should retrieve a float

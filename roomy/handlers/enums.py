from enum import Enum


class EventKey(str, Enum):
    """
    Constants representing events which may be called via ObserverHandler within this package
    """

    WILL_CHANGE_SCREEN = "will_change_screen"
    DID_CHANGE_SCREEN = "did_change_screen"

    WILL_CHANGE_ROOM = "will_change_room"
    DID_CHANGE_ROOM = "did_change_room"


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
    FRAME_DURATION_MS = "frame_duration_ms"  # Should retrieve an int

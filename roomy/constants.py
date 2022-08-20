class Constants:
    RESOURCE_FOLDER_PATH = "res"

    AUDIO_FREQUENCY = 88200

    COLOURS = {
        "dev": (0, 255, 0)
    }


class ErrorMessages:
    @staticmethod
    def stat_locked():
        raise PermissionError("cannot modify this object while .is_locked is set to a truthy value")

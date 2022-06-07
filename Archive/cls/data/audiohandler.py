from pygame import mixer

from ..constants import AudioStatuses


class AudioHandler:
    """
    Helper class which retrieves and stores Sound objects, and handles various aspects of Audio objects
    """

    # For performance optimisation. Stores sounds which have already been loaded before, using file paths as their keys
    SOUNDS = {}

    # Audio objects are stored in multiple ways to optimise for performance when querying for them
    AUDIO_OBJECTS = set()
    AUDIO_OBJECTS_FROZEN = frozenset(AUDIO_OBJECTS)  # Should be updated whenever AUDIO_OBJECTS is altered
    AUDIO_BY_FILE_PATH = {}
    AUDIO_BY_ENTITY_ID = {}  # Uses IDs as keys so that it does not prevent the entity being garbage collected

    @staticmethod
    def add(audio: "Audio") -> None:
        """
        This method will be called automatically by Audio during normal execution, and does not need to be called
        elsewhere
        """

        AudioHandler.AUDIO_OBJECTS.add(audio)
        AudioHandler.AUDIO_OBJECTS_FROZEN = frozenset(AudioHandler.AUDIO_OBJECTS)

        if audio.file_path not in AudioHandler.AUDIO_BY_FILE_PATH:
            AudioHandler.AUDIO_BY_FILE_PATH[audio.file_path] = set()
        AudioHandler.AUDIO_BY_FILE_PATH[audio.file_path].add(audio)

        if not id(audio) in AudioHandler.AUDIO_BY_ENTITY_ID:
            AudioHandler.AUDIO_BY_ENTITY_ID[id(audio)] = set()
        AudioHandler.AUDIO_BY_ENTITY_ID[id(audio)].add(audio)

    @staticmethod
    def remove(audio: "Audio") -> None:
        """
        This method will be called automatically by Audio during normal execution.
        It can be called elsewhere to safely get rid of an Audio instance that has not yet begun playing
        """

        assert audio.status == AudioStatuses.STOPPED or not audio.is_playing, \
            "AudioHandler.remove() should only be called manually on Audio instances that have not begun playing"

        AudioHandler.AUDIO_OBJECTS.remove(audio)
        AudioHandler.AUDIO_OBJECTS_FROZEN = frozenset(AudioHandler.AUDIO_OBJECTS)

        AudioHandler.AUDIO_BY_FILE_PATH[audio.file_path].remove(audio)

        if audio in AudioHandler.AUDIO_BY_ENTITY_ID[id(audio)]:  # Necessary to account for delisted Audio instances
            AudioHandler.AUDIO_BY_ENTITY_ID[id(audio)].remove(audio)

    @staticmethod
    def update() -> None:
        """
        This method is to be called once per game tick, and will in turn update all Audio instances
        """

        for audio in AudioHandler.AUDIO_OBJECTS_FROZEN:
            audio.update()

    @staticmethod
    def delist_by_entity(entity: "Entity"):
        """
        This method is to be called in the destructor of Entity.
        It does not apply any changes to the relevant Audio instances,
        just delists them for the purposes of querying by entity. This is to prevent Audio instances from a now
        garbage-collected entity from being considered as assigned to a new entity due to an `id()` collision

        Because Audio instances are left unaffected by this method, any instances that are left unmanaged by their
        parent entity will simply play out as normal
        """

        if id(entity) in AudioHandler.AUDIO_BY_ENTITY_ID:
            del AudioHandler.AUDIO_BY_ENTITY_ID[id(entity)]

    @staticmethod
    def get_channel():
        """
        This method will be called in the constructor of Audio, to provide it with an idle (or new) Channel object
        """

        channel = mixer.find_channel()
        if channel:
            return channel

        mixer.set_num_channels(mixer.get_num_channels()+1)
        return mixer.Channel(mixer.get_num_channels()-1)

    @staticmethod
    def get_sound(audio: "Audio") -> mixer.Sound:
        """
        This method will be called in the constructor of Audio, to provide it with the relevant Sound object
        """

        AudioHandler._load_sound(audio.file_path)

        return AudioHandler.SOUNDS[audio.file_path]

    @staticmethod
    def _load_sound(file_path: str) -> None:
        """
        Loads a sound object for the file at the target file path, if it is not already loaded.
        """

        if file_path not in AudioHandler.SOUNDS:
            sound = mixer.Sound(file_path)

            AudioHandler.SOUNDS[file_path] = sound

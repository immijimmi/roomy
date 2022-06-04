from pygame import mixer

from weakref import ref

from ..constants import AudioStatuses
from ..data import AudioHandler
from ..methods import Methods


class Audio:
    """
    Each Audio object encapsulates one pygame Sound
    """

    def __init__(
            self, parent: "Entity", file_path: str,
            volume: float = 1.0, status: str = AudioStatuses.PLAYING,
            fade_ms: int = 1000
    ):
        self._is_playing = False  # Indicates whether the audio has ever begun playing
        self._is_paused = False  # Indicates whether the audio was previously playing and is now paused
        self._is_fading_out = False  # Indicates whether the audio was previously playing and is now fading out

        self.volume = volume  # Implemented as mono for the time being
        self.fade_ms = fade_ms  # Only used if status is set to .FADING_IN or .FADING_OUT

        self._file_path = file_path
        self._parent = ref(parent)  # Weakref so that it does not prevent parent object being garbage collected

        self._status = None
        self.status = status

        self._channel = AudioHandler.get_channel()
        self._sound = AudioHandler.get_sound(self)

        self._channel.set_volume(self.volume)
        AudioHandler.add(self)

        self.update()  # AudioHandler will make any successive calls to .update()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        assert value in Methods.get_class_attrs(AudioStatuses).values(), f"invalid Audio status: {value}"

        if self._status == AudioStatuses.FADING_OUT:  # This is checking the *current* status, not checking `value`
            raise RuntimeError("Audio status cannot be changed once it has begun fading out")

        if not self._is_playing:
            if value not in AudioStatuses.VALID_INITIAL_STATUSES:
                raise ValueError(f"initial Audio status must be one of {AudioStatuses.VALID_INITIAL_STATUSES}")
        else:
            if value == AudioStatuses.FADING_IN:
                raise ValueError("Audio cannot fade in once it has already begun playing")

        self._status = value

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    @property
    def parent(self) -> "Entity":
        return self._parent()

    @property
    def file_path(self) -> str:
        return self._file_path

    def update(self):
        """
        This method will be called by AudioHandler once per game tick
        """

        if not self._is_playing:
            # Status handling
            if self.status == AudioStatuses.FADING_IN:
                self._channel.play(self._sound, fade_ms=self.fade_ms)
                self._is_playing = True
                self.status = AudioStatuses.PLAYING

            elif self.status == AudioStatuses.PLAYING:
                self._channel.play(self._sound)
                self._is_playing = True

            elif self.status == AudioStatuses.PAUSED:
                pass

        else:
            # Pause handling
            if self.status == AudioStatuses.PAUSED and not self._is_paused:
                self._channel.pause()
                self._is_paused = True

            elif self.status not in AudioStatuses.SILENT_STATUSES and self._is_paused:
                self._channel.unpause()
                self._is_paused = False

            # Status handling
            if self.status == AudioStatuses.PAUSED:
                pass

            elif self.status == AudioStatuses.PLAYING:
                if self._channel.get_volume() != self.volume:
                    self._channel.set_volume(self.volume)

            elif self.status == AudioStatuses.FADING_OUT:
                if not self._is_fading_out:
                    self._channel.fadeout(self.fade_ms)
                    self._is_fading_out = True

                else:
                    if not self._channel.get_busy():
                        self._stop()

            elif self.status == AudioStatuses.STOPPED:
                self._stop()

    def _stop(self):
        self._channel.stop()

        AudioHandler.remove(self)

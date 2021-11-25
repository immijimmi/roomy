from pygame import mixer

from weakref import ref

from ..data import AudioHandler
from .constants import AudioStatuses


class Audio:
    """
    Each Audio object encapsulates one pygame Sound
    """

    def __init__(
            self, parent: "Entity.with_extensions(Animated)", file_name: str,
            volume: float = 1.0, status: str = AudioStatuses.PLAYING,
            full_fade_ms: int = 1000
    ):
        self.volume = volume  # No support for stereo volume as of yet
        self.status = status
        self.full_fade_ms = full_fade_ms  # Dictates the time a fade from 0% to 100% or vice versa would take.

        self._file_name = file_name
        self._parent = ref(parent)  # Weakref so that it does not prevent parent object being garbage collected
        self._is_paused = False

        self._channel = mixer.Channel(hash(self))
        self._sound = AudioHandler.get_sound(self)
        if self.status != AudioStatuses.PLAYING:
            self._channel.set_volume(0)

        AudioHandler.add(self)

        self._channel.play(self._sound)
        self.update(0)  # AudioHandler will make any successive calls to .update()

    @property
    def parent(self) -> "Entity.with_extensions(Animated)":
        return self._parent()

    @property
    def file_name(self) -> str:
        return self._file_name

    def update(self, elapsed_ms: int):
        # Pausing logic
        if self._is_paused:
            if self.status != AudioStatuses.PAUSED:
                self._channel.unpause()
                self._is_paused = False
        else:
            if self.status == AudioStatuses.PAUSED:
                self._channel.pause()
                self._is_paused = True

        # Individual status logic
        if self.status == AudioStatuses.PAUSED:
            pass  # Status is handled above

        elif self.status == AudioStatuses.PLAYING:
            if self._channel.get_volume() != self.volume:
                self._channel.set_volume(self.volume)

        elif self.status == AudioStatuses.FADING_IN:
            if (curr_volume := self._channel.get_volume()) != self.volume:
                volume_diff = self.volume - curr_volume
                max_fade = min(1.0, elapsed_ms / self.full_fade_ms)

                positive_capped_fade = min(max_fade, volume_diff)
                capped_fade = max(-max_fade, positive_capped_fade)  # Capped in both positive and negative directions

                self._channel.set_volume(curr_volume + capped_fade)

            if curr_volume == self.volume:
                self.status = AudioStatuses.PLAYING

        elif self.status == AudioStatuses.FADING_OUT:
            if (curr_volume := self._channel.get_volume()) != 0:
                volume_diff = 0 - curr_volume
                max_fade = min(1.0, elapsed_ms / self.full_fade_ms)

                positive_capped_fade = min(max_fade, volume_diff)
                capped_fade = max(-max_fade, positive_capped_fade)  # Capped in both positive and negative directions

                self._channel.set_volume(curr_volume + capped_fade)

            if curr_volume == 0:
                self.status = AudioStatuses.STOPPED
                self._stop()

        elif self.status == AudioStatuses.STOPPED:
            self._stop()

        else:
            raise ValueError(self.status)

    def _stop(self):
        self._sound.stop()
        self._channel.stop()

        AudioHandler.remove(self)

from pygame import mixer

from .constants import AudioStatuses


class Audio:
    def __init__(
            self, handler, file_name: str, volume: float = 1.0,
            status: str = AudioStatuses.PLAYING, full_fade_ms: int = 1000
    ):
        self.volume = volume
        self.status = status
        self.full_fade_ms = full_fade_ms  # Dictates the time a fade from 0% to 100% or vice versa would take.

        self._file_name = file_name
        self._handler = handler
        self._is_paused = False

        self._channel = mixer.Channel(hash(self))
        self._sound = mixer.Sound(self._file_name)
        if self.status == AudioStatuses.FADING_IN:
            self._sound.set_volume(0)

        self._channel.play(self._sound)
        self.update(0)

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
            if self._sound.get_volume() != self.volume:
                self._sound.set_volume(self.volume)

        elif self.status == AudioStatuses.FADING_IN:
            if (curr_volume := self._sound.get_volume()) != self.volume:
                volume_diff = self.volume - curr_volume
                max_fade = min(1.0, elapsed_ms / self.full_fade_ms)

                positive_capped_fade = min(max_fade, volume_diff)
                capped_fade = max(-max_fade, positive_capped_fade)  # Capped in both positive and negative directions

                self._sound.set_volume(curr_volume + capped_fade)

            if curr_volume == self.volume:
                self.status = AudioStatuses.PLAYING

        elif self.status == AudioStatuses.FADING_OUT:
            if (curr_volume := self._sound.get_volume()) != 0:
                volume_diff = 0 - curr_volume
                max_fade = min(1.0, elapsed_ms / self.full_fade_ms)

                positive_capped_fade = min(max_fade, volume_diff)
                capped_fade = max(-max_fade, positive_capped_fade)  # Capped in both positive and negative directions

                self._sound.set_volume(curr_volume + capped_fade)

            if curr_volume == 0:
                self._stop()
                self.status = AudioStatuses.STOPPED

        elif self.status == AudioStatuses.STOPPED:
            self._stop()

        else:
            raise ValueError(self.status)

    def _stop(self):
        self._sound.stop()
        self._channel.stop()

        self._handler.remove(self)

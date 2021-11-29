class AudioStatuses:
    """
    Constants representing statuses used by Audio objects
    """

    STOPPED = "stopped"  # Permanently halts playback
    PAUSED = "paused"  # Temporarily halts playback
    PLAYING = "playing"
    FADING_IN = "fading_in"
    FADING_OUT = "fading_out"

    # Status groups
    VALID_INITIAL_STATUSES = (FADING_IN, PLAYING, PAUSED)  # Before audio has begun playing, only use these statuses
    SILENT_STATUSES = (PAUSED, STOPPED)

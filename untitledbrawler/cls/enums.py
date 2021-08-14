from enum import Enum


class AnimationOnFinish(Enum):
    REPEAT = "repeat"
    HANG = "hang"  # Makes the animation stay on the last frame for that animation
    EXPIRE = "expire"  # Makes the animation change to a default/idle animation

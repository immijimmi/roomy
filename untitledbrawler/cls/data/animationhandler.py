from pygame import Surface, image

from json import loads
from typing import List

from ..enums import AnimationOnFinish


class AnimationHandler:
    """
    Helper class which calculates what animation frame an instance should be displaying,
    as well as storing loaded frames for reuse
    """

    # For performance optimisation, stores frames which have already been loaded under their file paths as keys
    frames = {}
    # Similar optimisation for storing frame filename lists
    frame_filenames = {}

    @staticmethod
    def get_frame(target_instance: "Entity.with_extensions(Animated)") -> Surface:
        target_class_name = target_instance.__class__.__name__

        frame_filenames_list = AnimationHandler._get_or_load_frame_filenames(target_instance)
        total_frames = len(frame_filenames_list)

        frames_elapsed = int(
            target_instance.animation.elapsed_effective / target_instance.animation.frame_time
        )

        if target_instance.animation.on_finish == AnimationOnFinish.REPEAT:
            frame_number = frames_elapsed % total_frames
        elif target_instance.animation.on_finish == AnimationOnFinish.HANG:
            frame_number = min(total_frames-1, frames_elapsed)
        else:
            raise NotImplementedError

        # Standardised animation frame file path structure
        frame_file_path = rf"res\{target_class_name}\{frame_filenames_list[frame_number]}"

        return AnimationHandler._get_or_load_frame(frame_file_path)

    @staticmethod
    def _get_or_load_frame(file_path: str) -> Surface:
        if file_path not in AnimationHandler.frames:
            AnimationHandler.frames[file_path] = image.load(file_path).convert_alpha()

        return AnimationHandler.frames[file_path]

    @staticmethod
    def _get_or_load_frame_filenames(target_instance: "Entity.with_extensions(Animated)") -> List[str]:
        """
        Returns only the list of frame filenames for the specific animation in question, however if data needs to be
        loaded from file it is done in chunks containing data for every animation associated with the target class
        """

        target_class_name = target_instance.__class__.__name__
        animation_key = target_instance.animation.key

        if target_class_name not in AnimationHandler.frame_filenames:
            with open(rf"res\{target_class_name}\animation_data.json", "r") as file:
                data = loads(file.read())
                AnimationHandler.frame_filenames[target_class_name] = data

        return AnimationHandler.frame_filenames[target_class_name][animation_key]

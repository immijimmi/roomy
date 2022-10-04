from pygame import image


class Methods:
    @staticmethod
    def load_image(file_path: str):
        """
        Wrapper method for pygame.image.load() which takes only a `str` file path, and provides a more informative
        error message when the file cannot be found
        """

        try:
            image.load(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"unable to locate a file under the following path: {file_path}")

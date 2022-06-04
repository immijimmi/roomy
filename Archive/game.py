class Game:
    def update(self):
        AudioHandler.update()  # Audio is handled at the top level since it may persist between screens

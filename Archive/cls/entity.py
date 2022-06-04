class Entity:
    def __del__(self):
        # May be removed if audio should continue playing when an entity is deleted
        AudioHandler.delist_by_entity(self)

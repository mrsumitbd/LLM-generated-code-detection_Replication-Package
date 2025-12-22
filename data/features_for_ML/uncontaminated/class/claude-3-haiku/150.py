class DeckContainer:
    def __init__(self, rotation: dict, **kwargs):
        self.rotation = rotation
        self.decks = kwargs

    def get_rotation(self):
        return self.rotation
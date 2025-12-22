class DeckContainer:
    def __init__(self, rotation: dict, **kwargs):
        if not isinstance(rotation, dict):
            raise TypeError("rotation must be a dict")
        self.rotation = rotation
        self.kwargs = kwargs

    def get_rotation(self):
        return self.rotation
class DeckContainer:
    
    def __init__(self, rotation: dict, **kwargs):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation
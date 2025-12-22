class ThingManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.things = []

    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)
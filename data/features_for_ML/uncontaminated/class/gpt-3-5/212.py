class Thing:
    def __init__(self, name):
        self.name = name

class ThingManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThingManager()
        return cls._instance

    def __init__(self):
        self.things = []

    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

# Example usage:
# thing_manager = ThingManager.get_instance()
# thing1 = Thing("Chair")
# thing2 = Thing("Table")
# thing_manager.add_thing(thing1)
# thing_manager.add_thing(thing2)
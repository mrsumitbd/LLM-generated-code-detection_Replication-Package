class ThingManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        """Return the singleton instance of ThingManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the ThingManager with an empty collection."""
        self._things = []

    def add_thing(self, thing):
        """Add a thing to the manager.

        Args:
            thing: The thing to add. No type enforcement is performed.
        """
        self._things.append(thing)
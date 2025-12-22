class NoUpdate:
    """No update available."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return "No update available."

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, NoUpdate)

    def __hash__(self):
        return hash(self.__class__)
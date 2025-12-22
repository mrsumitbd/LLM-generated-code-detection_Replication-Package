class Command:
    """
    A simple command representation that stores a textual command and an identifier.
    """

    def __init__(self, _text, _id):
        if not isinstance(_text, str):
            raise TypeError(f"_text must be a str, got {type(_text).__name__}")
        if not isinstance(_id, (int, str)):
            raise TypeError(f"_id must be an int or str, got {type(_id).__name__}")

        self._text = _text
        self._id = _id

    @property
    def text(self):
        """Return the command text."""
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError(f"text must be a str, got {type(value).__name__}")
        self._text = value

    @property
    def id(self):
        """Return the command identifier."""
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, (int, str)):
            raise TypeError(f"id must be an int or str, got {type(value).__name__}")
        self._id = value

    def __repr__(self):
        return f"{self.__class__.__name__}(text={self._text!r}, id={self._id!r})"

    def __str__(self):
        return self._text

    def __eq__(self, other):
        if not isinstance(other, Command):
            return NotImplemented
        return self._id == other._id and self._text == other._text

    def __hash__(self):
        return hash((self._id, self._text))

    def to_dict(self):
        """Return a dictionary representation of the command."""
        return {"id": self._id, "text": self._text}

    @classmethod
    def from_dict(cls, data):
        """Create a Command instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")
        if "id" not in data or "text" not in data:
            raise ValueError("Dictionary must contain 'id' and 'text' keys")
        return cls(data["text"], data["id"])
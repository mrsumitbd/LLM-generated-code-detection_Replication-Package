class SokakuAdditionalAbilityIBRecord:
    """
    A flexible record class that stores arbitrary attributes.
    """

    def __init__(self, **kwargs):
        # Store all provided keyword arguments in a private dictionary.
        super().__setattr__("_data", {})
        for key, value in kwargs.items():
            self._data[key] = value

    # Attribute access
    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    # Dictionary conversion
    def to_dict(self):
        """Return a shallow copy of the internal data dictionary."""
        return dict(self._data)

    @classmethod
    def from_dict(cls, data):
        """Create a new instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("from_dict expects a dict")
        return cls(**data)

    # Representation
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self._data.items())
        return f"{self.__class__.__name__}({attrs})"

    # Equality and hashing
    def __eq__(self, other):
        if isinstance(other, SokakuAdditionalAbilityIBRecord):
            return self._data == other._data
        return False

    def __hash__(self):
        return hash(frozenset(self._data.items()))

    # Miscellaneous helpers
    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
class BaseBuffRecord:
    """基础记录Class"""

    def __init__(self, **kwargs):
        # Store all attributes in a private dictionary
        super().__setattr__('_data', {})
        for key, value in kwargs.items():
            self._data[key] = value

    # Attribute access
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        if name in self._data:
            del self._data[name]
        else:
            super().__delattr__(name)

    # Dictionary-like interface
    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def to_dict(self):
        return dict(self._data)

    # Representation
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self._data.items())
        return f'{self.__class__.__name__}({attrs})'

    # Equality
    def __eq__(self, other):
        if not isinstance(other, BaseBuffRecord):
            return NotImplemented
        return self._data == other._data

    # Iteration over keys
    def __iter__(self):
        return iter(self._data)

    # Length
    def __len__(self):
        return len(self._data)

    # Membership test
    def __contains__(self, key):
        return key in self._data
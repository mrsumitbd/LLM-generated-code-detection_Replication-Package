class JsonHParams:
    def __init__(self, **kwargs):
        self._data = dict(kwargs)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data!r})"
class JsonHParams:
    def __init__(self, **kwargs):
        self._params = kwargs

    def keys(self):
        return self._params.keys()

    def items(self):
        return self._params.items()

    def values(self):
        return self._params.values()

    def __len__(self):
        return len(self._params)

    def __getitem__(self, key):
        return self._params[key]

    def __setitem__(self, key, value):
        self._params[key] = value

    def __contains__(self, key):
        return key in self._params

    def __repr__(self):
        return f"JsonHParams({self._params})"
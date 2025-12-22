class SMState:
    """State machine state container."""

    def __init__(self):
        self._state = None
        self._data = {}

    def reset(self) -> None:
        self._state = None
        self._data.clear()

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def set_data(self, key, value):
        self._data[key] = value

    def get_data(self, key, default=None):
        return self._data.get(key, default)

    def clear_data(self):
        self._data.clear()

    def __repr__(self):
        return f"SMState(state={self._state}, data={self._data})"
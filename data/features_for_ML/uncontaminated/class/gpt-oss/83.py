class SMState:
    """State machine state container."""

    def __init__(self) -> None:
        self._state: str | None = None
        self._vars: dict[str, object] = {}

    def reset(self) -> None:
        """Reset the state machine to its initial state."""
        self._state = None
        self._vars.clear()

    def set_state(self, state: str) -> None:
        """Set the current state."""
        self._state = state

    def get_state(self) -> str | None:
        """Return the current state."""
        return self._state

    def set_var(self, key: str, value: object) -> None:
        """Set a variable in the state container."""
        self._vars[key] = value

    def get_var(self, key: str, default: object | None = None) -> object | None:
        """Get a variable from the state container."""
        return self._vars.get(key, default)

    def __repr__(self) -> str:
        return f"<SMState state={self._state!r} vars={self._vars!r}>"
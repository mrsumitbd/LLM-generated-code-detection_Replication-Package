class DoAccountAuthResponse:
    def __init__(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        self._data = data
        self.success = data.get("success", False)
        self.token = data.get("token")
        self.error = data.get("error")
        self.user_id = data.get("user_id")
        self.message = data.get("message")

    def is_successful(self) -> bool:
        return bool(self.success)

    def to_dict(self) -> dict:
        return dict(self._data)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"success={self.success!r}, token={self.token!r}, "
            f"error={self.error!r}, user_id={self.user_id!r}, "
            f"message={self.message!r})"
        )

    def __str__(self) -> str:
        return f"DoAccountAuthResponse(success={self.success}, token={self.token})"

    def __getattr__(self, name: str):
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)
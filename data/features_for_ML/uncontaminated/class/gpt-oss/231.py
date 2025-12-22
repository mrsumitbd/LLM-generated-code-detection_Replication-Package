class Key:
    """Key object compatible with pywidevine."""

    def __init__(self, kid: str, key: str, type_: str = "CONTENT"):
        """
        Create a Key instance.

        Parameters
        ----------
        kid : str
            Hexadecimal representation of the Key ID.
        key : str
            Hexadecimal representation of the key data.
        type_ : str, optional
            Type of the key (default is "CONTENT").
        """
        if not isinstance(kid, str):
            raise TypeError(f"kid must be a hex string, got {type(kid).__name__}")
        if not isinstance(key, str):
            raise TypeError(f"key must be a hex string, got {type(key).__name__}")

        try:
            self.kid = bytes.fromhex(kid)
        except ValueError as exc:
            raise ValueError(f"Invalid hex string for kid: {kid}") from exc

        try:
            self.key = bytes.fromhex(key)
        except ValueError as exc:
            raise ValueError(f"Invalid hex string for key: {key}") from exc

        if not isinstance(type_, str):
            raise TypeError(f"type_ must be a string, got {type(type_).__name__}")
        self.type_ = type_

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(kid={self.kid.hex()}, "
            f"key={self.key.hex()}, type_={self.type_!r})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return (
            self.kid == other.kid
            and self.key == other.key
            and self.type_ == other.type_
        )
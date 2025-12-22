from uuid import UUID

class Key:
    """Key object compatible with pywidevine."""

    def __init__(self, kid: str, key: str, type_: str = "CONTENT"):
        if isinstance(kid, str):
            clean_kid = kid.replace("-", "")
            if len(clean_kid) == 32:
                self.kid = UUID(hex=clean_kid)
            else:
                self.kid = UUID(hex=clean_kid.ljust(32, "0"))
        else:
            self.kid = kid

        if isinstance(key, str):
            self.key = bytes.fromhex(key)
        else:
            self.key = key

        self.type = type_
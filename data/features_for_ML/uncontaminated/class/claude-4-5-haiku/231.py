class Key:
    """Key object compatible with pywidevine."""

    def __init__(self, kid: str, key: str, type_: str = "CONTENT"):
        self.kid = kid
        self.key = key
        self.type_ = type_
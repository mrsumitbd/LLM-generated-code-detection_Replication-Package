class Config:
    """SQLModel configuration."""

    def __init__(self, db_url: str, debug: bool = False):
        self.db_url = db_url
        self.debug = debug

    def __repr__(self):
        return f"Config(db_url='{self.db_url}', debug={self.debug})"

    def __str__(self):
        return f"Database URL: {self.db_url}, Debug: {self.debug}"
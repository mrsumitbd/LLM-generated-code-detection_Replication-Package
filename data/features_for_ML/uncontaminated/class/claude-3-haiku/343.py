class NoUpdate:
    """No update available."""

    def __init__(self):
        self.available = False
        self.version = "N/A"
        self.release_date = "N/A"

    def check_update(self):
        return self.available

    def get_version(self):
        return self.version

    def get_release_date(self):
        return self.release_date
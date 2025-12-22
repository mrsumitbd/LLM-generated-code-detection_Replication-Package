class App:
    def __init__(self, manager: StreamableHTTPSessionManager) -> None:
        self.manager = manager
        self.session = manager.get_session()

    def get_session(self):
        return self.session

    def close(self):
        if hasattr(self.session, "close"):
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
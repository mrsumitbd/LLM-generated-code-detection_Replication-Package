from contextlib import contextmanager

class GlobalSettings:

    @staticmethod
    def get() -> Settings:
        pass

    @staticmethod
    @contextmanager
    def push():
        pass
class Dummy:
    def __init_subclass__(cls, **kwargs):
        raise TypeError("Subclassing of Dummy is not allowed")
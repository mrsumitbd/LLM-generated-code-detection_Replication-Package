
class WatchDog:
    def __init__(self, **kwargs):
        try:
            watch_reverse_order(**kwargs)
        except AttributeError:
            pass
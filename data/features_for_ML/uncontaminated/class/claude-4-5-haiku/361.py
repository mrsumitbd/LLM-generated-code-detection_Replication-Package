class WorkerRunData:
    def __init__(self):
        self._stopped = False
        self._print_key = None

    def _to_print_key(self):
        if self._print_key is None:
            self._print_key = id(self)
        return self._print_key

    @property
    def stopped(self):
        return self._stopped
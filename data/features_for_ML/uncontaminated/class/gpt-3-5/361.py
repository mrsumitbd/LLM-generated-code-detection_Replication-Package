class WorkerRunData:

    def __init__(self):
        self._stopped = False

    def _to_print_key(self):
        pass

    @property
    def stopped(self):
        return self._stopped
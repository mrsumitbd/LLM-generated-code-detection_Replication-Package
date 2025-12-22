class NCCLIDStore:
    def __init__(self, nccl_id):
        self._nccl_id = nccl_id
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            return self._nccl_id
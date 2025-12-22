class NCCLIDStore:
    def __init__(self, nccl_id):
        if not isinstance(nccl_id, (bytes, bytearray, str)):
            raise TypeError("nccl_id must be bytes, bytearray, or str")
        self._nccl_id = nccl_id

    def get(self):
        return self._nccl_id

class NCCLIDStore:

    def __init__(self, nccl_id):
        self._nccl_id = nccl_id

    def get(self):
        return self._nccl_id
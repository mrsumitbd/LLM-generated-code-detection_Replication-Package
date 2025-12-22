class NCCLIDStore:

    def __init__(self, nccl_id):
        self.nccl_id = nccl_id

    def get(self):
        return self.nccl_id
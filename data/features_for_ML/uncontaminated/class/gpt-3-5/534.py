import torch

class T3Cond:
    """
    Dataclass container for most / all conditioning info.
    TODO: serialization methods aren't used, keeping them around for convenience
    """

    def __init__(self, data):
        self.data = data

    def to(self, *, device=None, dtype=None):
        self.data = self.data.to(device=device, dtype=dtype)
        return self

    def save(self, fpath):
        torch.save(self.data, fpath)

    @staticmethod
    def load(fpath, map_location="cpu"):
        data = torch.load(fpath, map_location=map_location)
        return T3Cond(data)
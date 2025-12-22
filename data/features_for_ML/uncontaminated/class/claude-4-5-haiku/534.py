class T3Cond:
    """
    Dataclass container for most / all conditioning info.
    TODO: serialization methods aren't used, keeping them around for convenience
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to(self, *, device=None, dtype=None):
        import torch
        
        result = T3Cond()
        for key, value in self.__dict__.items():
            if isinstance(value, torch.Tensor):
                if device is not None:
                    value = value.to(device=device)
                if dtype is not None:
                    value = value.to(dtype=dtype)
            setattr(result, key, value)
        return result

    def save(self, fpath):
        import torch
        
        state_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, torch.Tensor):
                state_dict[key] = value.cpu()
            else:
                state_dict[key] = value
        torch.save(state_dict, fpath)

    @staticmethod
    def load(fpath, map_location="cpu"):
        import torch
        
        state_dict = torch.load(fpath, map_location=map_location)
        cond = T3Cond()
        for key, value in state_dict.items():
            setattr(cond, key, value)
        return cond
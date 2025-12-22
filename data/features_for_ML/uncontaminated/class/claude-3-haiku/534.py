import torch

class T3Cond:
    """
    Dataclass container for most / all conditioning info.
    TODO: serialization methods aren't used, keeping them around for convenience
    """
    def __init__(self, cond_emb, cond_mask, cond_pos_emb, cond_attn_mask):
        self.cond_emb = cond_emb
        self.cond_mask = cond_mask
        self.cond_pos_emb = cond_pos_emb
        self.cond_attn_mask = cond_attn_mask

    def to(self, *, device=None, dtype=None):
        if device is not None:
            self.cond_emb = self.cond_emb.to(device=device)
            self.cond_mask = self.cond_mask.to(device=device)
            self.cond_pos_emb = self.cond_pos_emb.to(device=device)
            self.cond_attn_mask = self.cond_attn_mask.to(device=device)
        if dtype is not None:
            self.cond_emb = self.cond_emb.to(dtype=dtype)
            self.cond_mask = self.cond_mask.to(dtype=dtype)
            self.cond_pos_emb = self.cond_pos_emb.to(dtype=dtype)
            self.cond_attn_mask = self.cond_attn_mask.to(dtype=dtype)
        return self

    def save(self, fpath):
        torch.save(self.__dict__, fpath)

    @staticmethod
    def load(fpath, map_location="cpu"):
        state_dict = torch.load(fpath, map_location=map_location)
        instance = T3Cond.__new__(T3Cond)
        instance.__dict__.update(state_dict)
        return instance
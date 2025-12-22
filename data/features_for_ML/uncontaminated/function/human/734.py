import torch
from einops import rearrange

def transpose(tensor):
            tensor = rearrange(tensor, "(b v) (h w) c -> b v h w c", v=num_views, h=height)
            tensor_0, tensor_1 = torch.chunk(tensor, dim=0, chunks=2)  # b v h w c
            tensor = torch.cat([tensor_0, tensor_1], dim=3)  # b v h 2w c
            tensor = rearrange(tensor, "b v h w c -> (b h) (v w) c", v=num_views, h=height)
            return tensor
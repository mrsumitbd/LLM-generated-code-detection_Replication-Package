import torch

def keep(conf):
    BLOCK_N_Q = conf.kwargs["BLOCK_N_Q"]
    BLOCK_N_KV = conf.kwargs["BLOCK_N_KV"]
    return not (is_cuda() and torch.cuda.get_device_capability()[0] == 9 and BLOCK_N_Q * BLOCK_N_KV < 128 * 128
                and conf.num_warps == 8)
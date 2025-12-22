import torch
from megatron.core import mpu
from megatron.core import mpu

def broadcast_params(module):
        for param in module.parameters():
            torch.distributed.broadcast(param.data,
                                        src=mpu.get_data_parallel_src_rank(),
                                        group=mpu.get_data_parallel_group())
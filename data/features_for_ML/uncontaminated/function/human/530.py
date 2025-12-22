import torch
from cuda import cuda, cudart
from triton_dist.utils import (CUDA_CHECK, NVSHMEM_SIGNAL_DTYPE, has_fullmesh_nvlink, get_numa_world_size,
                               nvshmem_barrier_all_on_stream, sleep_async)

def set_ready(rank, segment, stream: torch.cuda.Stream):
        (err, ) = write_value_fn(
            stream.cuda_stream,
            barrier_buffers[rank][segment].data_ptr(),
            1,
            cuda.CUstreamWriteValue_flags.CU_STREAM_WRITE_VALUE_DEFAULT,
        )
        CUDA_CHECK(err)
import torch
import dataclasses
from typing import Optional, List
from triton_dist.kernels.nvidia.common_ops import BarrierAllContext, barrier_all_on_stream
from triton_dist.utils import initialize_distributed, nvshmem_barrier_all_on_stream, NVSHMEM_SIGNAL_DTYPE, nvshmem_create_tensors, nvshmem_free_tensor_sync

class ReduceScatter2DContext:
    max_M: int
    N: int
    rank: int
    world_size: int
    local_world_size: int
    dtype: torch.dtype
    overlap_with_gemm: bool

    # comm buffer
    symm_scatter_bufs: List[torch.Tensor]
    symm_rs_per_node_bufs: List[torch.Tensor]
    symm_p2p_bufs: List[torch.Tensor]

    # barrier bufs
    symm_signal_bufs: List[
        torch.
        Tensor]  # need reset: signal_buf =  scatter_signal | rs_per_node_signal
    barrier: BarrierAllContext

    # stream
    reduction_stream: torch.cuda.Stream
    p2p_stream: torch.cuda.Stream

    # sms
    num_sync_sms: int
    num_p2p_sms: int
    num_reduction_sms: int

    # preprocess to reduce cpu overhead
    # comm barriers
    symm_scatter_signal_bufs: List[torch.Tensor] = dataclasses.field(
        init=False)
    symm_rs_per_node_signal_bufs: List[torch.Tensor] = dataclasses.field(
        init=False)

    local_rank: int = dataclasses.field(init=False)
    node_id: int = dataclasses.field(init=False)
    nnodes: int = dataclasses.field(init=False)

    scatter_signal_buf_list_for_each_node: List[
        torch.Tensor] = dataclasses.field(init=False)

    def __post_init__(self):
        self.local_rank = self.rank % self.local_world_size
        self.node_id = self.rank // self.local_world_size
        self.nnodes = self.world_size // self.local_world_size
        self.scatter_signal_buf_list_for_each_node = []
        for buf in self.symm_signal_bufs:
            assert buf.shape[0] >= 2 * self.world_size

        self.symm_scatter_signal_bufs = [
            buf[:self.world_size] for buf in self.symm_signal_bufs
        ]
        self.symm_rs_per_node_signal_bufs = [
            buf[self.world_size:self.world_size * 2]
            for buf in self.symm_signal_bufs
        ]

        for node_id in range(self.nnodes):
            self.scatter_signal_buf_list_for_each_node.append(
                self.symm_scatter_signal_bufs[self.local_rank]
                [node_id * self.local_world_size:(node_id + 1) *
                 self.local_world_size])

    def finalize(self):
        nvshmem_free_tensor_sync(self.symm_scatter_bufs[self.local_rank])
        nvshmem_free_tensor_sync(self.symm_rs_per_node_bufs[self.local_rank])
        nvshmem_free_tensor_sync(self.symm_p2p_bufs[self.local_rank])
        nvshmem_free_tensor_sync(self.symm_signal_bufs[self.local_rank])

    def reset_barriers(self):
        self.symm_signal_bufs[self.local_rank].fill_(0)

    def get_scatter_bufs_and_signal_for_each_node(self, input, node_id):
        M = input.shape[0]
        M_per_rank = M // self.world_size
        M_per_node = M_per_rank * self.local_world_size
        scatter_bufs_intra_node = [
            self.symm_scatter_bufs[i][node_id * M_per_node:(node_id + 1) *
                                      M_per_node]
            for i in range(self.local_world_size)
        ]
        return scatter_bufs_intra_node, self.scatter_signal_buf_list_for_each_node[
            node_id]

    @property
    def symm_rs_per_node_buf(self) -> torch.Tensor:
        return self.symm_rs_per_node_bufs[self.local_rank]

    @property
    def symm_rs_per_node_signal_buf(self) -> torch.Tensor:
        return self.symm_rs_per_node_signal_bufs[self.local_rank]

    @property
    def symm_p2p_buf(self) -> torch.Tensor:
        return self.symm_p2p_bufs[self.local_rank]

    @property
    def num_rs_sms(self) -> int:
        if self.nnodes > 1:
            return self.num_sync_sms + self.num_p2p_sms + self.num_reduction_sms
        else:
            # for intra node rs, no sm required.
            return 0

    @property
    def symm_scatter_signal_buf(self) -> torch.Tensor:
        return self.symm_scatter_signal_bufs[self.local_rank]
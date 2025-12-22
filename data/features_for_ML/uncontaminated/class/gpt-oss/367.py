import torch
from dataclasses import dataclass, field

@dataclass
class ReduceScatter2DContext:
    num_nodes: int = 1
    num_sms: int = 1
    buffer_size: int = 1024
    device: torch.device = field(default_factory=lambda: torch.device("cpu"))

    _symm_rs_per_node_buf: torch.Tensor = field(init=False, repr=False)
    _symm_rs_per_node_signal_buf: torch.Tensor = field(init=False, repr=False)
    _symm_p2p_buf: torch.Tensor = field(init=False, repr=False)
    _symm_scatter_signal_buf: torch.Tensor = field(init=False, repr=False)

    def __post_init__(self):
        self._symm_rs_per_node_buf = torch.zeros(
            (self.num_nodes, self.buffer_size), device=self.device
        )
        self._symm_rs_per_node_signal_buf = torch.zeros(
            (self.num_nodes,), dtype=torch.bool, device=self.device
        )
        self._symm_p2p_buf = torch.zeros(
            (self.num_nodes, self.num_nodes, self.buffer_size), device=self.device
        )
        self._symm_scatter_signal_buf = torch.zeros(
            (self.num_nodes,), dtype=torch.bool, device=self.device
        )

    def finalize(self):
        # Release buffers
        del self._symm_rs_per_node_buf
        del self._symm_rs_per_node_signal_buf
        del self._symm_p2p_buf
        del self._symm_scatter_signal_buf

    def reset_barriers(self):
        self._symm_rs_per_node_signal_buf.zero_()
        self._symm_scatter_signal_buf.zero_()

    def get_scatter_bufs_and_signal_for_each_node(self, input: torch.Tensor, node_id: int):
        if node_id < 0 or node_id >= self.num_nodes:
            raise IndexError("node_id out of range")
        # Copy input into the per‑node buffer
        self._symm_rs_per_node_buf[node_id].copy_(input)
        return self._symm_rs_per_node_buf[node_id], self._symm_rs_per_node_signal_buf[node_id]

    @property
    def symm_rs_per_node_buf(self) -> torch.Tensor:
        return self._symm_rs_per_node_buf

    @property
    def symm_rs_per_node_signal_buf(self) -> torch.Tensor:
        return self._symm_rs_per_node_signal_buf

    @property
    def symm_p2p_buf(self) -> torch.Tensor:
        return self._symm_p2p_buf

    @property
    def num_rs_sms(self) -> int:
        return self.num_sms

    @property
    def symm_scatter_signal_buf(self) -> torch.Tensor:
        return self._symm_scatter_signal_buf
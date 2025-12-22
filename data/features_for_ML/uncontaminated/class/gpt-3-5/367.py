import torch

class ReduceScatter2DContext:

    def __post_init__(self):
        self.symm_rs_per_node_buf = None
        self.symm_rs_per_node_signal_buf = None
        self.symm_p2p_buf = None
        self.num_rs_sms = 0
        self.symm_scatter_signal_buf = None

    def finalize(self):
        pass

    def reset_barriers(self):
        pass

    def get_scatter_bufs_and_signal_for_each_node(self, input, node_id):
        pass

    @property
    def symm_rs_per_node_buf(self) -> torch.Tensor:
        return self.symm_rs_per_node_buf

    @property
    def symm_rs_per_node_signal_buf(self) -> torch.Tensor:
        return self.symm_rs_per_node_signal_buf

    @property
    def symm_p2p_buf(self) -> torch.Tensor:
        return self.symm_p2p_buf

    @property
    def num_rs_sms(self) -> int:
        return self.num_rs_sms

    @property
    def symm_scatter_signal_buf(self) -> torch.Tensor:
        return self.symm_scatter_signal_buf
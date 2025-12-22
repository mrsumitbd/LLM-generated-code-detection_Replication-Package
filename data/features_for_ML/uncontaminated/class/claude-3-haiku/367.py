import torch

class ReduceScatter2DContext:
    def __init__(self, num_rs_sms: int, device: torch.device):
        self.num_rs_sms = num_rs_sms
        self.device = device
        self.__post_init__()

    def __post_init__(self):
        self.symm_rs_per_node_buf = torch.zeros(self.num_rs_sms, device=self.device)
        self.symm_rs_per_node_signal_buf = torch.zeros(self.num_rs_sms, device=self.device)
        self.symm_p2p_buf = torch.zeros(self.num_rs_sms, device=self.device)
        self.symm_scatter_signal_buf = torch.zeros(self.num_rs_sms, device=self.device)
        self.reset_barriers()

    def finalize(self):
        pass

    def reset_barriers(self):
        self.symm_rs_per_node_buf.zero_()
        self.symm_rs_per_node_signal_buf.zero_()
        self.symm_p2p_buf.zero_()
        self.symm_scatter_signal_buf.zero_()

    def get_scatter_bufs_and_signal_for_each_node(self, input, node_id):
        self.symm_rs_per_node_buf[node_id] = input
        self.symm_rs_per_node_signal_buf[node_id] = 1.0
        return self.symm_rs_per_node_buf, self.symm_rs_per_node_signal_buf, self.symm_p2p_buf, self.symm_scatter_signal_buf
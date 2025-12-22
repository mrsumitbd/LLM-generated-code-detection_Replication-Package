class ReduceScatter2DContext:
    def __init__(self):
        self._symm_rs_per_node_buf = None
        self._symm_rs_per_node_signal_buf = None
        self._symm_p2p_buf = None
        self._num_rs_sms = 0
        self._symm_scatter_signal_buf = None
        self._barriers = []
        self._scatter_bufs = {}
        self._scatter_signals = {}

    def __post_init__(self):
        self._barriers = []
        self._scatter_bufs = {}
        self._scatter_signals = {}

    def finalize(self):
        if self._symm_rs_per_node_buf is not None:
            self._symm_rs_per_node_buf = None
        if self._symm_rs_per_node_signal_buf is not None:
            self._symm_rs_per_node_signal_buf = None
        if self._symm_p2p_buf is not None:
            self._symm_p2p_buf = None
        if self._symm_scatter_signal_buf is not None:
            self._symm_scatter_signal_buf = None
        self._barriers.clear()
        self._scatter_bufs.clear()
        self._scatter_signals.clear()

    def reset_barriers(self):
        self._barriers = []

    def get_scatter_bufs_and_signal_for_each_node(self, input, node_id):
        if node_id not in self._scatter_bufs:
            self._scatter_bufs[node_id] = input
        if node_id not in self._scatter_signals:
            self._scatter_signals[node_id] = None
        return self._scatter_bufs[node_id], self._scatter_signals[node_id]

    @property
    def symm_rs_per_node_buf(self) -> torch.Tensor:
        return self._symm_rs_per_node_buf

    @symm_rs_per_node_buf.setter
    def symm_rs_per_node_buf(self, value: torch.Tensor):
        self._symm_rs_per_node_buf = value

    @property
    def symm_rs_per_node_signal_buf(self) -> torch.Tensor:
        return self._symm_rs_per_node_signal_buf

    @symm_rs_per_node_signal_buf.setter
    def symm_rs_per_node_signal_buf(self, value: torch.Tensor):
        self._symm_rs_per_node_signal_buf = value

    @property
    def symm_p2p_buf(self) -> torch.Tensor:
        return self._symm_p2p_buf

    @symm_p2p_buf.setter
    def symm_p2p_buf(self, value: torch.Tensor):
        self._symm_p2p_buf = value

    @property
    def num_rs_sms(self) -> int:
        return self._num_rs_sms

    @num_rs_sms.setter
    def num_rs_sms(self, value: int):
        self._num_rs_sms = value

    @property
    def symm_scatter_signal_buf(self) -> torch.Tensor:
        return self._symm_scatter_signal_buf

    @symm_scatter_signal_buf.setter
    def symm_scatter_signal_buf(self, value: torch.Tensor):
        self._symm_scatter_signal_buf = value
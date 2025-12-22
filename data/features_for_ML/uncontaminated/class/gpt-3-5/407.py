import torch
from model_config import ModelConfig
from model_builder import ModelBuilder
from paged_kv_cache import PagedKVCache

class Qwen3Model:
    """
    Qwen3 model implementation for tensor parallel training.
    This model initializes the parameters, sets the forward pass method, and provides an inference method.
    It supports both torch and triton_dist modes for forward pass.
    """

    def __init__(self, batch_size, model_config: ModelConfig, builder: 'ModelBuilder', build_lm_head=True) -> None:
        self.batch_size = batch_size
        self.model_config = model_config
        self.builder = builder
        self.build_lm_head = build_lm_head

    def init_parameters(self):
        # Initialize parameters here
        pass

    def build_fwd(self, hidden_states: torch.Tensor, kv_cache: PagedKVCache):
        # Build forward pass here
        pass

    def mega_forwrad(self, input_ids: torch.LongTensor):
        # Perform inference here
        pass
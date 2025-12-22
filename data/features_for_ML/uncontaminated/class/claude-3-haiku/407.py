import torch

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

        self.init_parameters()

    def init_parameters(self):
        # Initialize the model parameters
        self.transformer = self.builder.build_transformer(self.model_config)
        self.lm_head = self.builder.build_lm_head(self.model_config) if self.build_lm_head else None

    def build_fwd(self, hidden_states: torch.Tensor, kv_cache: PagedKVCache):
        # Implement the forward pass method
        output = self.transformer(hidden_states, kv_cache)
        if self.lm_head:
            output = self.lm_head(output)
        return output

    def mega_forwrad(self, input_ids: torch.LongTensor):
        # Implement the inference method
        kv_cache = self.builder.build_kv_cache(self.batch_size, self.model_config)
        hidden_states = self.transformer.forward_with_cache(input_ids, kv_cache)
        output = self.build_fwd(hidden_states, kv_cache)
        return output
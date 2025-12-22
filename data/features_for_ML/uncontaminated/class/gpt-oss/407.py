import torch
from typing import List, Optional

# Assume these types are defined elsewhere in the codebase
# from some_module import ModelConfig, ModelBuilder, PagedKVCache

class Qwen3Model:
    """
    Qwen3 model implementation for tensor parallel training.
    This model initializes the parameters, sets the forward pass method,
    and provides an inference method.
    It supports both torch and triton_dist modes for forward pass.
    """

    def __init__(
        self,
        batch_size: int,
        model_config: "ModelConfig",
        builder: "ModelBuilder",
        build_lm_head: bool = True,
    ) -> None:
        self.batch_size = batch_size
        self.model_config = model_config
        self.builder = builder
        self.build_lm_head = build_lm_head

        # Build core components
        self.embedding = builder.build_embedding()
        self.layers: List[torch.nn.Module] = builder.build_layers()
        self.triton_dist = getattr(builder, "triton_dist", False)

        if build_lm_head:
            self.lm_head = builder.build_lm_head()
        else:
            self.lm_head = None

        # KV cache used during inference
        self.kv_cache: Optional["PagedKVCache"] = None

        # Initialize parameters
        self.init_parameters()

    # ------------------------------------------------------------------
    # Parameter initialization
    # ------------------------------------------------------------------
    def init_parameters(self) -> None:
        """
        Initialize all parameters in the model.
        """
        # Embedding layer
        if hasattr(self.embedding, "init_weights"):
            self.embedding.init_weights()

        # Transformer layers
        for layer in self.layers:
            if hasattr(layer, "init_weights"):
                layer.init_weights()

        # LM head
        if self.lm_head is not None and hasattr(self.lm_head, "init_weights"):
            self.lm_head.init_weights()

    # ------------------------------------------------------------------
    # Forward pass
    # ------------------------------------------------------------------
    def build_fwd(
        self,
        hidden_states: torch.Tensor,
        kv_cache: "PagedKVCache",
    ) -> torch.Tensor:
        """
        Forward pass through the transformer layers.
        Supports both torch and triton_dist modes.
        """
        if self.triton_dist:
            # Triton distributed forward
            return self._triton_forward(hidden_states, kv_cache)

        # Standard torch forward
        for layer in self.layers:
            hidden_states = layer(hidden_states, kv_cache)
        return hidden_states

    def _triton_forward(
        self,
        hidden_states: torch.Tensor,
        kv_cache: "PagedKVCache",
    ) -> torch.Tensor:
        """
        Triton distributed forward pass.
        Delegates to the builder's triton_forward implementation.
        """
        if hasattr(self.builder, "triton_forward"):
            return self.builder.triton_forward(hidden_states, kv_cache)
        raise NotImplementedError(
            "Triton forward is not implemented in the provided builder."
        )

    # ------------------------------------------------------------------
    # Inference / mega forward
    # ------------------------------------------------------------------
    def mega_forward(self, input_ids: torch.LongTensor) -> torch.Tensor:
        """
        Full inference pipeline: embedding -> transformer -> lm_head.
        """
        # Create or reuse KV cache
        if self.kv_cache is None:
            self.kv_cache = self.builder.build_kv_cache(
                batch_size=self.batch_size,
                seq_len=input_ids.size(1),
                num_heads=self.model_config.num_attention_heads,
                head_dim=self.model_config.head_dim,
            )

        # Embedding
        hidden_states = self.embedding(input_ids)

        # Transformer layers
        hidden_states = self.build_fwd(hidden_states, self.kv_cache)

        # LM head (if enabled)
        if self.lm_head is not None:
            logits = self.lm_head(hidden_states)
            return logits

        return hidden_states
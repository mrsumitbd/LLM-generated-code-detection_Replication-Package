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
        
        # Initialize model components
        self.embed_tokens = builder.build_embed_tokens(model_config)
        self.layers = torch.nn.ModuleList([
            builder.build_decoder_layer(model_config, i) 
            for i in range(model_config.num_hidden_layers)
        ])
        self.norm = builder.build_norm(model_config)
        
        if build_lm_head:
            self.lm_head = builder.build_lm_head(model_config)
        else:
            self.lm_head = None
        
        self.init_parameters()
        
        # Set forward method based on configuration
        if hasattr(model_config, 'forward_mode') and model_config.forward_mode == 'triton_dist':
            self.forward_fn = self._triton_dist_forward
        else:
            self.forward_fn = self._torch_forward

    def init_parameters(self):
        """Initialize model parameters with appropriate distributions."""
        for module in self.modules():
            if isinstance(module, torch.nn.Linear):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    torch.nn.init.zeros_(module.bias)
            elif isinstance(module, torch.nn.Embedding):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def build_fwd(self, hidden_states: torch.Tensor, kv_cache: PagedKVCache):
        """
        Build forward pass through the model layers.
        
        Args:
            hidden_states: Input hidden states tensor
            kv_cache: Paged KV cache for attention
            
        Returns:
            Output hidden states after passing through all layers
        """
        for i, layer in enumerate(self.layers):
            hidden_states = layer(hidden_states, kv_cache)
        
        # Apply final normalization
        hidden_states = self.norm(hidden_states)
        
        return hidden_states

    def _torch_forward(self, input_ids: torch.LongTensor, kv_cache: PagedKVCache = None):
        """Standard PyTorch forward pass."""
        hidden_states = self.embed_tokens(input_ids)
        hidden_states = self.build_fwd(hidden_states, kv_cache)
        
        if self.lm_head is not None:
            logits = self.lm_head(hidden_states)
        else:
            logits = hidden_states
        
        return logits

    def _triton_dist_forward(self, input_ids: torch.LongTensor, kv_cache: PagedKVCache = None):
        """Triton distributed forward pass."""
        hidden_states = self.embed_tokens(input_ids)
        hidden_states = self.build_fwd(hidden_states, kv_cache)
        
        if self.lm_head is not None:
            logits = self.lm_head(hidden_states)
        else:
            logits = hidden_states
        
        return logits

    def mega_forwrad(self, input_ids: torch.LongTensor):
        """
        Mega forward pass for inference.
        
        Args:
            input_ids: Input token IDs
            
        Returns:
            Model output logits
        """
        kv_cache = PagedKVCache(
            num_layers=self.model_config.num_hidden_layers,
            num_heads=self.model_config.num_attention_heads,
            head_dim=self.model_config.hidden_size // self.model_config.num_attention_heads,
            batch_size=self.batch_size
        )
        
        return self.forward_fn(input_ids, kv_cache)
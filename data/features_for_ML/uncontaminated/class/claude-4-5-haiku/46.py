class FlopsCounter:
    """
    Used to count mfu during training loop

    Example:
        flops_counter = FlopsCounter(config)
        flops_achieved, flops_promised = flops_counter.estimate_flops(tokens_list, delta_time)

    """

    def __init__(self, config: PretrainedConfig):
        self.config = config
        self.hidden_size = config.hidden_size
        self.num_hidden_layers = config.num_hidden_layers
        self.vocab_size = config.vocab_size
        self.intermediate_size = getattr(config, 'intermediate_size', None)
        self.model_name = getattr(config, 'model_type', 'unknown')
        
        # Calculate intermediate size if not provided
        if self.intermediate_size is None:
            if hasattr(config, 'hidden_act'):
                # For models like Qwen2, calculate based on hidden_size
                self.intermediate_size = int(8 * self.hidden_size / 3)
            else:
                self.intermediate_size = 4 * self.hidden_size

    def _estimate_unknown_flops(self, tokens_sum, batch_seqlens, delta_time):
        """
        Estimate FLOPs for unknown model architecture using standard transformer formula.
        FLOPs = 6 * N * D where N is tokens and D is model parameters
        """
        # Calculate total parameters
        # Embedding: vocab_size * hidden_size
        # Transformer layers: num_layers * (attention + feedforward)
        # Attention: 3 * hidden_size^2 (Q, K, V projections)
        # Feedforward: 2 * hidden_size * intermediate_size
        # Output layer: hidden_size * vocab_size
        
        params = (self.vocab_size * self.hidden_size +
                 self.num_hidden_layers * (3 * self.hidden_size ** 2 + 
                                          2 * self.hidden_size * self.intermediate_size) +
                 self.hidden_size * self.vocab_size)
        
        # Standard formula: 6 FLOPs per parameter per token
        flops_promised = 6 * tokens_sum * params
        flops_achieved = flops_promised / delta_time if delta_time > 0 else 0
        
        return flops_achieved, flops_promised

    def _estimate_qwen2_flops(self, tokens_sum, batch_seqlens, delta_time):
        """
        Estimate FLOPs for Qwen2 model architecture.
        Qwen2 uses specific attention and feedforward patterns.
        """
        # Qwen2 specific calculation
        # Forward pass FLOPs per token:
        # - Embedding lookup: hidden_size
        # - Each transformer layer:
        #   - Attention: 4 * hidden_size^2 (Q, K, V, O projections)
        #   - Feedforward: 2 * hidden_size * intermediate_size
        # - Output projection: hidden_size * vocab_size
        
        flops_per_token = (
            self.hidden_size +  # embedding
            self.num_hidden_layers * (
                4 * self.hidden_size ** 2 +  # attention
                2 * self.hidden_size * self.intermediate_size  # feedforward
            ) +
            self.hidden_size * self.vocab_size  # output
        )
        
        # Total FLOPs for forward pass
        flops_promised = tokens_sum * flops_per_token
        
        # Account for backward pass (approximately 2x forward)
        flops_promised *= 3  # 1x forward + 2x backward
        
        flops_achieved = flops_promised / delta_time if delta_time > 0 else 0
        
        return flops_achieved, flops_promised

    def estimate_flops(self, batch_seqlens, delta_time):
        """
        Estimate achieved and promised FLOPs based on batch sequence lengths and time.
        
        Args:
            batch_seqlens: List of sequence lengths in the batch
            delta_time: Time elapsed in seconds
            
        Returns:
            Tuple of (flops_achieved, flops_promised)
        """
        # Calculate total tokens
        tokens_sum = sum(batch_seqlens) if isinstance(batch_seqlens, (list, tuple)) else batch_seqlens
        
        # Route to appropriate estimation method based on model type
        if 'qwen' in self.model_name.lower():
            flops_achieved, flops_promised = self._estimate_qwen2_flops(tokens_sum, batch_seqlens, delta_time)
        else:
            flops_achieved, flops_promised = self._estimate_unknown_flops(tokens_sum, batch_seqlens, delta_time)
        
        return flops_achieved, flops_promised
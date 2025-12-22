from transformers import PretrainedConfig

class FlopsCounter:
    """
    Used to count mfu during training loop

    Example:
        flops_counter = FlopsCounter(config)
        flops_achieved, flops_promised = flops_counter.estimate_flops(tokens_list, delta_time)

    """

    def __init__(self, config: PretrainedConfig):
        self.config = config

    def _estimate_unknown_flops(self, tokens_sum, batch_seqlens, delta_time):
        # Implementation for estimating unknown flops
        pass

    def _estimate_qwen2_flops(self, tokens_sum, batch_seqlens, delta_time):
        # Implementation for estimating qwen2 flops
        pass

    def estimate_flops(self, batch_seqlens, delta_time):
        # Implementation for estimating total flops
        flops_achieved = self._estimate_unknown_flops(sum(batch_seqlens), batch_seqlens, delta_time)
        flops_promised = self._estimate_qwen2_flops(sum(batch_seqlens), batch_seqlens, delta_time)
        return flops_achieved, flops_promised
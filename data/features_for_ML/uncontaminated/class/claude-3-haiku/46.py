import math

class FlopsCounter:
    """
    Used to count mfu during training loop

    Example:
        flops_counter = FlopsCounter(config)
        flops_achieved, flops_promised = flops_counter.estimate_flops(tokens_list, delta_time)

    """

    def __init__(self, config: PretrainedConfig):
        self.config = config
        self.flops_promised = config.max_flops
        self.flops_achieved = 0

    def _estimate_unknown_flops(self, tokens_sum, batch_seqlens, delta_time):
        unknown_flops = tokens_sum * self.config.unknown_flops_per_token
        return unknown_flops

    def _estimate_qwen2_flops(self, tokens_sum, batch_seqlens, delta_time):
        qwen2_flops = tokens_sum * self.config.qwen2_flops_per_token
        return qwen2_flops

    def estimate_flops(self, batch_seqlens, delta_time):
        tokens_sum = sum(batch_seqlens)
        unknown_flops = self._estimate_unknown_flops(tokens_sum, batch_seqlens, delta_time)
        qwen2_flops = self._estimate_qwen2_flops(tokens_sum, batch_seqlens, delta_time)
        self.flops_achieved = unknown_flops + qwen2_flops
        return self.flops_achieved, self.flops_promised
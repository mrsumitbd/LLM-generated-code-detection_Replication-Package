from typing import Tuple, Optional
from transformers import PretrainedConfig


class FlopsCounter:
    """
    Used to count MFU during training loop.

    Example:
        flops_counter = FlopsCounter(config)
        flops_achieved, flops_promised = flops_counter.estimate_flops(batch_seqlens, delta_time)
    """

    def __init__(self, config: PretrainedConfig):
        """
        Initialize the counter with a model configuration.

        Parameters
        ----------
        config : PretrainedConfig
            The configuration of the model.  The counter uses the
            configuration to determine how to estimate FLOPs for
            specific model families.
        """
        self.config = config
        # Determine the estimation strategy based on the model type
        self._estimate_fn = self._estimate_unknown_flops
        if getattr(config, "model_type", "").lower() == "qwen2":
            self._estimate_fn = self._estimate_qwen2_flops

    def _estimate_unknown_flops(
        self, tokens_sum: int, batch_seqlens: list[int], delta_time: float
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Fallback estimation when the model type is unknown.

        Returns
        -------
        Tuple[None, None]
            Indicates that no FLOPs estimate could be produced.
        """
        return None, None

    def _estimate_qwen2_flops(
        self, tokens_sum: int, batch_seqlens: list[int], delta_time: float
    ) -> Tuple[float, float]:
        """
        Estimate FLOPs for Qwen2 models.

        The estimate is based on a simplified transformer FLOPs
        calculation:
            * Self‑attention: 3 * hidden_size^2 per token per layer
            * Feed‑forward: 4 * hidden_size * intermediate_size per token per layer

        Parameters
        ----------
        tokens_sum : int
            Total number of tokens in the batch.
        batch_seqlens : list[int]
            Sequence lengths of each example in the batch.
        delta_time : float
            Time elapsed for the batch in seconds.

        Returns
        -------
        Tuple[float, float]
            (flops_achieved, flops_promised) in MFU (million FLOPs per second).
        """
        hidden_size = getattr(self.config, "hidden_size", 4096)
        intermediate_size = getattr(self.config, "intermediate_size", 16384)
        num_layers = getattr(self.config, "num_hidden_layers", 32)

        # FLOPs per token per layer
        flops_per_token_per_layer = (
            3 * hidden_size * hidden_size + 4 * hidden_size * intermediate_size
        )

        # Total FLOPs for the batch
        total_flops = tokens_sum * flops_per_token_per_layer * num_layers

        # Convert to MFU (million FLOPs per second)
        flops_achieved = total_flops / delta_time / 1e6
        # For Qwen2 we assume the promised FLOPs equals the achieved FLOPs
        flops_promised = flops_achieved

        return flops_achieved, flops_promised

    def estimate_flops(
        self, batch_seqlens: list[int], delta_time: float
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Estimate the FLOPs for a training batch.

        Parameters
        ----------
        batch_seqlens : list[int]
            Sequence lengths of each example in the batch.
        delta_time : float
            Time elapsed for the batch in seconds.

        Returns
        -------
        Tuple[Optional[float], Optional[float]]
            (flops_achieved, flops_promised) in MFU.  If the model type is
            unknown, both values will be ``None``.
        """
        tokens_sum = sum(batch_seqlens)
        return self._estimate_fn(tokens_sum, batch_seqlens, delta_time)
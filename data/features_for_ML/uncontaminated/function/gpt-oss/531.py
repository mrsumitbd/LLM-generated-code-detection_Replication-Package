import torch
import numpy as np
import numpy.typing as npt

# Constants expected to be defined elsewhere in the package.
# Import them if available; otherwise, raise an informative error.
try:
    from .constants import (
        EEGPT_TOKEN_DIM,
        EEGPT_SUMMARY_TOKENS,
        EEGPT_PROBE_INPUT_DIM,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(
        "Required constants EEGPT_TOKEN_DIM, EEGPT_SUMMARY_TOKENS, "
        "and EEGPT_PROBE_INPUT_DIM are missing."
    ) from exc


def prepare_probe_features(
    features: npt.NDArray[np.float32] | npt.NDArray[np.float64] | torch.Tensor,
) -> torch.Tensor:
    """Prepare EEGPT features for probe consumption.

    This is the SSOT adapter that ensures features are always in the correct
    shape (B, EEGPT_PROBE_INPUT_DIM) for probes, regardless of input shape.

    Args:
        features: EEGPT features in one of these shapes:
            - (EEGPT_TOKEN_DIM,): Single summary vector (will error - invalid)
            - (EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM): Single sample, 4 tokens
            - (EEGPT_PROBE_INPUT_DIM,): Single sample, already flattened
            - (B, EEGPT_TOKEN_DIM): Batch of summaries (will error - invalid)
            - (B, EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM): Batch of 4 tokens each
            - (B, EEGPT_PROBE_INPUT_DIM): Batch, already flattened

    Returns:
        Torch tensor of shape (B, EEGPT_PROBE_INPUT_DIM) ready for probe consumption.

    Raises:
        ValueError: If features have invalid shape (e.g., EEGPT_TOKEN_DIM-d summaries).
    """
    # Convert to torch tensor if necessary
    if isinstance(features, torch.Tensor):
        x = features
    else:
        # Assume numpy array
        x = torch.from_numpy(features).float()

    # Ensure dtype is float32
    if x.dtype != torch.float32:
        x = x.float()

    shape = x.shape

    # Helper to flatten a single sample of tokens
    def flatten_single(sample: torch.Tensor) -> torch.Tensor:
        return sample.reshape(-1)

    # Case 1: 1D tensor
    if x.ndim == 1:
        if shape[0] == EEGPT_PROBE_INPUT_DIM:
            # Already flattened single sample
            return x.unsqueeze(0)
        elif shape[0] == EEGPT_TOKEN_DIM:
            raise ValueError(
                f"Invalid shape: single summary vector of length {EEGPT_TOKEN_DIM}."
            )
        else:
            raise ValueError(
                f"Invalid 1D shape: expected {EEGPT_PROBE_INPUT_DIM} or {EEGPT_TOKEN_DIM}, got {shape[0]}."
            )

    # Case 2: 2D tensor
    if x.ndim == 2:
        # (EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM) -> single sample
        if shape == (EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM):
            return flatten_single(x).unsqueeze(0)

        # (B, EEGPT_PROBE_INPUT_DIM) -> already flattened batch
        if shape[1] == EEGPT_PROBE_INPUT_DIM:
            return x

        # (B, EEGPT_TOKEN_DIM) -> batch of summaries (invalid)
        if shape[1] == EEGPT_TOKEN_DIM:
            raise ValueError(
                f"Invalid batch shape: expected (B, {EEGPT_PROBE_INPUT_DIM}) or (B, {EEGPT_SUMMARY_TOKENS}, {EEGPT_TOKEN_DIM}), got (B, {EEGPT_TOKEN_DIM})."
            )

        # (B, EEGPT_TOKEN_DIM) where B == EEGPT_SUMMARY_TOKENS -> single sample
        if shape[0] == EEGPT_SUMMARY_TOKENS and shape[1] == EEGPT_TOKEN_DIM:
            return flatten_single(x).unsqueeze(0)

        raise ValueError(f"Invalid 2D shape: {shape}")

    # Case 3: 3D tensor
    if x.ndim == 3:
        # (B, EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM) -> batch of 4 tokens each
        if shape[1] == EEGPT_SUMMARY_TOKENS and shape[2] == EEGPT_TOKEN_DIM:
            return x.reshape(shape[0], -1)

        raise ValueError(f"Invalid 3D shape: {shape}")

    raise ValueError(f"Unsupported tensor dimensionality: {x.ndim}")
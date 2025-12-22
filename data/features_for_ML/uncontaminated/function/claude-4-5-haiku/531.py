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
    # Convert to torch tensor if needed
    if isinstance(features, np.ndarray):
        features = torch.from_numpy(features)
    
    # Get constants from the module
    from eegpt.constants import EEGPT_TOKEN_DIM, EEGPT_SUMMARY_TOKENS, EEGPT_PROBE_INPUT_DIM
    
    # Handle different input shapes
    if features.dim() == 1:
        # 1D tensor: either (EEGPT_TOKEN_DIM,) or (EEGPT_PROBE_INPUT_DIM,)
        if features.shape[0] == EEGPT_TOKEN_DIM:
            # Invalid: single summary vector
            raise ValueError(
                f"Invalid feature shape {features.shape}. "
                f"Cannot process single summary vector of shape ({EEGPT_TOKEN_DIM},). "
                f"Expected either ({EEGPT_SUMMARY_TOKENS}, {EEGPT_TOKEN_DIM}) or ({EEGPT_PROBE_INPUT_DIM},)."
            )
        elif features.shape[0] == EEGPT_PROBE_INPUT_DIM:
            # Single sample, already flattened - add batch dimension
            return features.unsqueeze(0)
        else:
            raise ValueError(
                f"Invalid 1D feature shape {features.shape}. "
                f"Expected ({EEGPT_PROBE_INPUT_DIM},)."
            )
    
    elif features.dim() == 2:
        # 2D tensor: either (B, EEGPT_TOKEN_DIM), (B, EEGPT_PROBE_INPUT_DIM), or (EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM)
        if features.shape[1] == EEGPT_TOKEN_DIM:
            if features.shape[0] == EEGPT_SUMMARY_TOKENS:
                # Single sample with 4 tokens - flatten and add batch dimension
                return features.reshape(1, -1)
            else:
                # Invalid: batch of summaries
                raise ValueError(
                    f"Invalid feature shape {features.shape}. "
                    f"Cannot process batch of summary vectors with shape (B, {EEGPT_TOKEN_DIM}). "
                    f"Expected ({EEGPT_SUMMARY_TOKENS}, {EEGPT_TOKEN_DIM}) or (B, {EEGPT_PROBE_INPUT_DIM})."
                )
        elif features.shape[1] == EEGPT_PROBE_INPUT_DIM:
            # Batch, already flattened
            return features
        else:
            raise ValueError(
                f"Invalid 2D feature shape {features.shape}. "
                f"Expected (B, {EEGPT_PROBE_INPUT_DIM}) or ({EEGPT_SUMMARY_TOKENS}, {EEGPT_TOKEN_DIM})."
            )
    
    elif features.dim() == 3:
        # 3D tensor: (B, EEGPT_SUMMARY_TOKENS, EEGPT_TOKEN_DIM)
        if features.shape[1] == EEGPT_SUMMARY_TOKENS and features.shape[2] == EEGPT_TOKEN_DIM:
            # Batch of 4 tokens each - flatten last two dimensions
            batch_size = features.shape[0]
            return features.reshape(batch_size, -1)
        else:
            raise ValueError(
                f"Invalid 3D feature shape {features.shape}. "
                f"Expected (B, {EEGPT_SUMMARY_TOKENS}, {EEGPT_TOKEN_DIM})."
            )
    
    else:
        raise ValueError(
            f"Invalid feature dimensionality {features.dim()}. "
            f"Expected 1D, 2D, or 3D tensor."
        )
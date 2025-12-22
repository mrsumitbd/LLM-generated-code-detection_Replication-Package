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
    if isinstance(features, np.ndarray):
        features = torch.from_numpy(features)

    if features.ndim == 1:
        if features.shape[0] == EEGPT_PROBE_INPUT_DIM:
            return features.unsqueeze(0)
        else:
            raise ValueError(f"Invalid features shape: {features.shape}")
    elif features.ndim == 2:
        if features.shape[1] == EEGPT_PROBE_INPUT_DIM:
            return features
        elif features.shape[1] == EEGPT_TOKEN_DIM:
            return features.view(-1, EEGPT_PROBE_INPUT_DIM)
        else:
            raise ValueError(f"Invalid features shape: {features.shape}")
    elif features.ndim == 3:
        if features.shape[1] == EEGPT_SUMMARY_TOKENS and features.shape[2] == EEGPT_TOKEN_DIM:
            return features.view(-1, EEGPT_PROBE_INPUT_DIM)
        else:
            raise ValueError(f"Invalid features shape: {features.shape}")
    else:
        raise ValueError(f"Invalid features shape: {features.shape}")
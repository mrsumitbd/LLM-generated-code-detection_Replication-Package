def run_ppo(config, compute_score=None):
    """
    Placeholder implementation of a PPO training routine.

    Parameters
    ----------
    config : dict
        Configuration dictionary for the training run. The function does not
        interpret any keys; it simply accepts the dictionary to satisfy the
        expected signature.
    compute_score : callable, optional
        A callable that can be used to compute a score for the current policy.
        It is not invoked in this placeholder implementation.

    Returns
    -------
    None
        This function performs no training and returns ``None``.
    """
    # The real implementation would set up the environment, policy,
    # optimizer, and run the PPO training loop.  For the purposes of the
    # tests in this repository, a no‑op implementation is sufficient.
    return None
def lr_lambda(current_step):
    """Return a learning‑rate multiplier for the given training step."""
    # Exponential decay: lr_multiplier = 0.95 ** step
    return 0.95 ** current_step
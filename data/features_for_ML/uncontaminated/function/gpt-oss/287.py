import os
import random

def set_all_random_seed(seed: int) -> None:
    """
    Set the random seed for all common random number generators used in Python
    projects, including the built‑in `random`, NumPy, PyTorch, and TensorFlow
    (if available).  The function also sets the `PYTHONHASHSEED` environment
    variable to ensure deterministic hashing.

    Parameters
    ----------
    seed : int
        The seed value to use for all RNGs.
    """
    # Set the environment variable for deterministic hashing
    os.environ["PYTHONHASHSEED"] = str(seed)

    # Built‑in random module
    random.seed(seed)

    # NumPy
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass

    # PyTorch
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        # Ensure deterministic behavior for CUDA kernels
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass

    # TensorFlow
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except Exception:
        pass

    # JAX
    try:
        import jax
        import jax.random as jr
        # JAX uses a PRNG key; we store it in an environment variable for reuse
        os.environ["JAX_PRNG_KEY"] = str(seed)
    except Exception:
        pass
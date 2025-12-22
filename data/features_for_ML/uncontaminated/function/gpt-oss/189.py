import random
import numpy as np

def sample_vectors(samples, num):
    """
    Randomly sample `num` vectors from `samples`.

    Parameters
    ----------
    samples : list or np.ndarray
        Collection of vectors to sample from.
    num : int
        Number of vectors to sample.

    Returns
    -------
    list or np.ndarray
        Sampled vectors. The type matches the input type.
    """
    if num <= 0:
        return [] if isinstance(samples, list) else np.empty((0, *np.shape(samples)[1:]))
    if isinstance(samples, np.ndarray):
        n = samples.shape[0]
        replace = num > n
        idx = np.random.choice(n, size=num, replace=replace)
        return samples[idx]
    else:  # assume list-like
        n = len(samples)
        if num <= n:
            return random.sample(samples, num)
        else:
            return random.choices(samples, k=num)
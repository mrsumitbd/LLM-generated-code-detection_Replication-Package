import numpy as np

def rand_gumbel_like(x):
    """
    Generate random samples from a standard Gumbel(0, 1) distribution
    with the same shape and dtype as the input array `x`.

    Parameters
    ----------
    x : array_like
        Reference array whose shape and dtype will be used for the output.

    Returns
    -------
    gumbel_samples : ndarray
        Random Gumbel samples with the same shape and dtype as `x`.
    """
    rng = np.random.default_rng()
    # Uniform samples in (0, 1)
    u = rng.uniform(size=np.shape(x))
    # Standard Gumbel: -log(-log(U))
    gumbel = -np.log(-np.log(u))
    # Ensure dtype matches the input
    return gumbel.astype(np.result_type(x), copy=False)
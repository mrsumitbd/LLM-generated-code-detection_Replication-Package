import numpy as np

def rand_gumbel_like(x):
    """
    Generate random samples from a standard Gumbel distribution with the same shape as `x`.

    Parameters
    ----------
    x : array_like
        Reference array whose shape determines the shape of the output.

    Returns
    -------
    out : ndarray
        Random Gumbel samples with the same shape as `x` and dtype matching `x`.
    """
    # Ensure we have a NumPy array to get dtype and shape
    x_arr = np.asarray(x)
    shape = x_arr.shape

    # Sample from uniform(0,1) and transform to Gumbel
    u = np.random.uniform(size=shape)
    gumbel = -np.log(-np.log(u))

    # Cast to the dtype of the input array
    return gumbel.astype(x_arr.dtype)
import random

def sample_vectors(samples, num):
    """
    Return a random sample of `num` vectors from the iterable `samples`.

    Parameters
    ----------
    samples : iterable
        An iterable of vectors (e.g., lists, tuples, numpy arrays, etc.).
    num : int
        The number of vectors to sample. Must be non‑negative and not larger
        than the number of available samples.

    Returns
    -------
    list
        A list containing `num` randomly selected vectors from `samples`.

    Raises
    ------
    ValueError
        If `num` is negative or greater than the number of available samples.
    """
    if num < 0:
        raise ValueError("num must be non‑negative")
    samples_list = list(samples)
    if num > len(samples_list):
        raise ValueError("num cannot be greater than the number of available samples")
    return random.sample(samples_list, num)
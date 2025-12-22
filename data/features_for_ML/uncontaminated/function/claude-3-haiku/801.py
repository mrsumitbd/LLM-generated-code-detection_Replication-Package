import random

def sample_vectors(samples, num):
    """
    Randomly sample a subset of vectors from the given list of samples.

    Args:
        samples (list): A list of vectors (represented as lists or tuples).
        num (int): The number of vectors to sample.

    Returns:
        list: A list of randomly sampled vectors.
    """
    return random.sample(samples, num)
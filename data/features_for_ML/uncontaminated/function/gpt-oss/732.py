import random
from typing import Tuple, List

def split_train_dev(
    samples: List["HallucinationSample"],
    dev_ratio: float = 0.1,
    seed: int = 42,
) -> Tuple[List["HallucinationSample"], List["HallucinationSample"]]:
    """
    Split the samples into train and dev sets.

    :param samples: List of HallucinationSample objects.
    :param dev_ratio: Ratio of the dev set.
    :param seed: Seed for the random number generator.
    :return: Tuple of train and dev sets.
    """
    # Make a copy to avoid mutating the original list
    shuffled = list(samples)
    rng = random.Random(seed)
    rng.shuffle(shuffled)

    # Determine the number of dev samples
    dev_size = int(len(shuffled) * dev_ratio)
    # Ensure at least one dev sample if ratio > 0 and list not empty
    if dev_ratio > 0 and dev_size == 0 and len(shuffled) > 0:
        dev_size = 1

    dev_set = shuffled[:dev_size]
    train_set = shuffled[dev_size:]
    return train_set, dev_set
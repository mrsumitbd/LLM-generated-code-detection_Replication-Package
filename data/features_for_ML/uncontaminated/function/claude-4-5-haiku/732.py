def split_train_dev(
    samples: list[HallucinationSample], dev_ratio: float = 0.1, seed: int = 42
) -> tuple[list[HallucinationSample], list[HallucinationSample]]:
    """Split the samples into train and dev sets.

    :param samples: List of HallucinationSample objects.
    :param dev_ratio: Ratio of the dev set.
    :param seed: Seed for the random number generator.
    :return: Tuple of train and dev sets.
    """
    import random
    
    random.seed(seed)
    
    dev_size = int(len(samples) * dev_ratio)
    
    shuffled_samples = samples.copy()
    random.shuffle(shuffled_samples)
    
    dev_set = shuffled_samples[:dev_size]
    train_set = shuffled_samples[dev_size:]
    
    return train_set, dev_set
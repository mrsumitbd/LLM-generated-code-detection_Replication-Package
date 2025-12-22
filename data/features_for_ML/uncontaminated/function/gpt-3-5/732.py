def split_train_dev(samples: list[HallucinationSample], dev_ratio: float = 0.1, seed: int = 42) -> tuple[list[HallucinationSample], list[HallucinationSample]]:
    import random
    random.seed(seed)
    random.shuffle(samples)
    dev_size = int(len(samples) * dev_ratio)
    dev_set = samples[:dev_size]
    train_set = samples[dev_size:]
    return train_set, dev_set
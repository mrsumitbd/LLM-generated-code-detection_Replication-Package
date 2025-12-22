import random
from lettucedetect.datasets.hallucination_dataset import (
    HallucinationData,
    HallucinationDataset,
    HallucinationSample,
)

def split_train_dev(
    samples: list[HallucinationSample], dev_ratio: float = 0.1, seed: int = 42
) -> tuple[list[HallucinationSample], list[HallucinationSample]]:
    """Split the samples into train and dev sets.

    :param samples: List of HallucinationSample objects.
    :param dev_ratio: Ratio of the dev set.
    :param seed: Seed for the random number generator.
    :return: Tuple of train and dev sets.
    """
    random.seed(seed)
    random.shuffle(samples)
    dev_size = int(len(samples) * dev_ratio)
    train_samples = samples[:-dev_size]
    dev_samples = samples[-dev_size:]
    return train_samples, dev_samples
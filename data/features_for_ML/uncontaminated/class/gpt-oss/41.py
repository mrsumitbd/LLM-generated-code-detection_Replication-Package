import random
import torch
from torch.utils.data import Dataset

class RealFakeDataset(Dataset):
    """
    A dataset that mixes real and fake image datasets according to a specified probability.
    Each returned sample is a tuple: (image, label, source_label), where `source_label`
    indicates the originating dataset index (or a custom mapping if provided).
    """

    def __init__(self, real_image_datasets: list, fake_image_datasets: list,
                 fake_prob=0.5, source_label_mapping=None):
        """
        Parameters
        ----------
        real_image_datasets : list
            List of datasets containing real images. Each dataset should return
            a tuple (image, label) or a single image.
        fake_image_datasets : list
            List of datasets containing fake images. Each dataset should return
            a tuple (image, label) or a single image.
        fake_prob : float, optional
            Probability of sampling from a fake dataset. Must be between 0 and 1.
        source_label_mapping : dict or None, optional
            Mapping from dataset index to a custom source label. If None, the
            dataset index itself is used as the source label.
        """
        self.real_datasets = real_image_datasets
        self.fake_datasets = fake_image_datasets
        self.fake_prob = float(fake_prob)
        if not (0.0 <= self.fake_prob <= 1.0):
            raise ValueError("fake_prob must be between 0 and 1")

        # Build a list of (dataset, source_label) tuples for real and fake
        self.real_sources = []
        self.fake_sources = []

        for idx, ds in enumerate(self.real_datasets):
            src_lbl = source_label_mapping.get(idx, idx) if source_label_mapping else idx
            self.real_sources.append((ds, src_lbl))

        for idx, ds in enumerate(self.fake_datasets):
            src_lbl = source_label_mapping.get(idx, idx) if source_label_mapping else idx
            self.fake_sources.append((ds, src_lbl))

        # Compute total length as sum of lengths of all underlying datasets
        self._len = sum(len(ds) for ds in self.real_datasets) + \
                    sum(len(ds) for ds in self.fake_datasets)

    def __len__(self):
        return self._len

    def __getitem__(self, index: int) -> tuple:
        """
        Returns a sample from either a real or fake dataset based on `fake_prob`.
        The returned tuple is (image, label, source_label).
        """
        # Decide whether to sample from fake or real
        if random.random() < self.fake_prob and self.fake_sources:
            ds, src_lbl = random.choice(self.fake_sources)
        else:
            ds, src_lbl = random.choice(self.real_sources)

        # Randomly pick an index within the chosen dataset
        if len(ds) == 0:
            raise IndexError("Selected dataset is empty.")
        idx = random.randint(0, len(ds) - 1)

        sample = ds[idx]
        # Handle dataset that returns only image
        if isinstance(sample, tuple):
            image, label = sample
        else:
            image, label = sample, None

        return image, label, src_lbl

    def reset(self):
        """
        Reset any internal state. For this dataset, nothing needs to be reset.
        """
        pass

    @staticmethod
    def collate_fn(batch):
        """
        Collate function to combine a list of samples into a batch.
        Expects each sample to be a tuple: (image, label, source_label).
        """
        images, labels, src_labels = zip(*batch)

        # Stack images (assumes all images have the same shape)
        images = torch.stack([torch.tensor(img) if not isinstance(img, torch.Tensor) else img
                              for img in images])

        # Convert labels and source labels to tensors if possible
        if all(isinstance(l, (int, float)) for l in labels):
            labels = torch.tensor(labels)
        else:
            labels = list(labels)

        if all(isinstance(l, (int, float)) for l in src_labels):
            src_labels = torch.tensor(src_labels)
        else:
            src_labels = list(src_labels)

        return images, labels, src_labels
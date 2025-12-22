import random

class RealFakeDataset:

    def __init__(self, real_image_datasets: list, fake_image_datasets: list, fake_prob=0.5, source_label_mapping=None):
        self.real_image_datasets = real_image_datasets
        self.fake_image_datasets = fake_image_datasets
        self.fake_prob = fake_prob
        self.source_label_mapping = source_label_mapping
        self.reset()

    def __getitem__(self, index: int) -> tuple:
        is_fake = random.random() < self.fake_prob
        if is_fake:
            dataset = random.choice(self.fake_image_datasets)
        else:
            dataset = random.choice(self.real_image_datasets)
        image, label = dataset[index % len(dataset)]
        if self.source_label_mapping is not None and label in self.source_label_mapping:
            label = self.source_label_mapping[label]
        return image, label

    def __len__(self) -> int:
        return max(len(dataset) for dataset in self.real_image_datasets + self.fake_image_datasets)

    def reset(self):
        for dataset in self.real_image_datasets + self.fake_image_datasets:
            dataset.reset()

    @staticmethod
    def collate_fn(batch):
        images, labels = zip(*batch)
        return torch.stack(images), torch.tensor(labels)
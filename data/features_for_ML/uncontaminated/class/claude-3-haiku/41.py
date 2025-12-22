import random

class RealFakeDataset:
    def __init__(self, real_image_datasets: list, fake_image_datasets: list, fake_prob=0.5, source_label_mapping=None):
        self.real_image_datasets = real_image_datasets
        self.fake_image_datasets = fake_image_datasets
        self.fake_prob = fake_prob
        self.source_label_mapping = source_label_mapping
        self.dataset_lengths = [len(dataset) for dataset in real_image_datasets + fake_image_datasets]
        self.total_length = sum(self.dataset_lengths)

    def __getitem__(self, index: int) -> tuple:
        is_fake = random.random() < self.fake_prob
        if is_fake:
            dataset_index = random.randint(0, len(self.fake_image_datasets) - 1)
            dataset = self.fake_image_datasets[dataset_index]
            label = 0
        else:
            dataset_index = random.randint(0, len(self.real_image_datasets) - 1)
            dataset = self.real_image_datasets[dataset_index]
            label = 1

        offset = sum(self.dataset_lengths[:dataset_index])
        item_index = (index - offset) % self.dataset_lengths[dataset_index]
        item = dataset[item_index]

        if self.source_label_mapping:
            label = self.source_label_mapping.get(label, label)

        return item, label

    def __len__(self) -> int:
        return self.total_length

    def reset(self):
        pass

    @staticmethod
    def collate_fn(batch):
        items, labels = zip(*batch)
        return items, labels
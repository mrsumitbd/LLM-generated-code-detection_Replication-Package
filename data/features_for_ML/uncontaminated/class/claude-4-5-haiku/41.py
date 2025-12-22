class RealFakeDataset:

    def __init__(self, real_image_datasets: list, fake_image_datasets: list, fake_prob=0.5, source_label_mapping=None):
        self.real_image_datasets = real_image_datasets
        self.fake_image_datasets = fake_image_datasets
        self.fake_prob = fake_prob
        self.source_label_mapping = source_label_mapping or {}
        
        self.real_indices = []
        self.fake_indices = []
        self.real_dataset_idx = []
        self.fake_dataset_idx = []
        
        for dataset_idx, dataset in enumerate(real_image_datasets):
            for sample_idx in range(len(dataset)):
                self.real_indices.append(sample_idx)
                self.real_dataset_idx.append(dataset_idx)
        
        for dataset_idx, dataset in enumerate(fake_image_datasets):
            for sample_idx in range(len(dataset)):
                self.fake_indices.append(sample_idx)
                self.fake_dataset_idx.append(dataset_idx)
        
        self.current_index = 0
        self.total_samples = len(self.real_indices) + len(self.fake_indices)

    def __getitem__(self, index: int) -> tuple:
        import random
        
        if random.random() < self.fake_prob:
            if len(self.fake_indices) == 0:
                dataset_type = 'real'
                dataset_list = self.real_image_datasets
                indices_list = self.real_indices
                dataset_idx_list = self.real_dataset_idx
                label = 0
            else:
                dataset_type = 'fake'
                dataset_list = self.fake_image_datasets
                indices_list = self.fake_indices
                dataset_idx_list = self.fake_dataset_idx
                label = 1
        else:
            if len(self.real_indices) == 0:
                dataset_type = 'fake'
                dataset_list = self.fake_image_datasets
                indices_list = self.fake_indices
                dataset_idx_list = self.fake_dataset_idx
                label = 1
            else:
                dataset_type = 'real'
                dataset_list = self.real_image_datasets
                indices_list = self.real_indices
                dataset_idx_list = self.real_dataset_idx
                label = 0
        
        local_index = index % len(indices_list) if len(indices_list) > 0 else 0
        dataset_idx = dataset_idx_list[local_index]
        sample_idx = indices_list[local_index]
        
        dataset = dataset_list[dataset_idx]
        sample = dataset[sample_idx]
        
        if isinstance(sample, tuple):
            image = sample[0]
            source_label = sample[1] if len(sample) > 1 else dataset_idx
        else:
            image = sample
            source_label = dataset_idx
        
        mapped_source_label = self.source_label_mapping.get(source_label, source_label)
        
        return image, label, mapped_source_label

    def __len__(self) -> int:
        return self.total_samples

    def reset(self):
        self.current_index = 0

    @staticmethod
    def collate_fn(batch):
        import torch
        from torch.utils.data.dataloader import default_collate
        
        images = []
        labels = []
        source_labels = []
        
        for item in batch:
            images.append(item[0])
            labels.append(item[1])
            source_labels.append(item[2])
        
        try:
            images = default_collate(images)
        except:
            images = images
        
        labels = torch.tensor(labels, dtype=torch.long)
        source_labels = torch.tensor(source_labels, dtype=torch.long)
        
        return images, labels, source_labels
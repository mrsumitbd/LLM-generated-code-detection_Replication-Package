import os
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader, random_split


class TransformedFeynmanDataModule:
    """
    A simple data module for loading and transforming Feynman data.
    """

    def __init__(
        self,
        data_path: str,
        batch_size: int = 32,
        transform=None,
        val_split: float = 0.2,
        test_split: float = 0.1,
    ):
        """
        Parameters
        ----------
        data_path : str
            Path to the CSV file containing the Feynman data.
        batch_size : int, optional
            Batch size for the data loaders.
        transform : callable, optional
            A function that takes a pandas DataFrame and returns a transformed DataFrame.
        val_split : float, optional
            Fraction of the data to use for validation.
        test_split : float, optional
            Fraction of the data to use for testing.
        """
        self.data_path = data_path
        self.batch_size = batch_size
        self.transform = transform
        self.val_split = val_split
        self.test_split = test_split

        self.train_dataset = None
        self.val_dataset = None
        self.test_dataset = None

    def setup(self):
        """
        Load the data, apply the optional transform, and split into train/val/test sets.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        df = pd.read_csv(self.data_path)

        if self.transform is not None:
            df = self.transform(df)

        # Convert DataFrame to a tensor dataset
        data_tensor = torch.tensor(df.values, dtype=torch.float32)
        dataset = TensorDataset(data_tensor)

        n_total = len(dataset)
        n_test = int(n_total * self.test_split)
        n_val = int(n_total * self.val_split)
        n_train = n_total - n_val - n_test

        self.train_dataset, self.val_dataset, self.test_dataset = random_split(
            dataset, [n_train, n_val, n_test]
        )

    @property
    def name(self):
        """
        Return the name of the data module.
        """
        return "TransformedFeynmanDataModule"

    # Optional convenience methods for data loaders
    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)
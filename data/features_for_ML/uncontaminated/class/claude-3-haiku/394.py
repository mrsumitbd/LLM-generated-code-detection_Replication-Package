import os
import numpy as np
import pandas as pd
from typing import Tuple

class HelpSteer3Dataset:
    """HelpSteer3 preference dataset for DPO training."""

    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        self.data = self.load_data()
        self.num_samples = len(self.data)

    def load_data(self) -> pd.DataFrame:
        """Load the HelpSteer3 preference dataset."""
        data_path = os.path.join(self.data_dir, 'helpsteer3_dataset.csv')
        return pd.read_csv(data_path)

    def get_sample(self, idx: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get a sample from the dataset."""
        row = self.data.iloc[idx]
        return (
            row['image_1'].astype(np.float32),
            row['image_2'].astype(np.float32),
            row['preference'].astype(np.float32)
        )

    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return self.num_samples

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get a sample from the dataset."""
        return self.get_sample(idx)
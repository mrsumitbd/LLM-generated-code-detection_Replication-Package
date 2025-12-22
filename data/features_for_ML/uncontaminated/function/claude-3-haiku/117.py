import os
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple

def Dataset(data_list_file: str,
            data_pipeline: callable,
            mode: str = 'train',
            gan: bool = False,
            shuffle: bool = True,
            partition: bool = True,
            tts_file: str = '',
            prompt_utt2data: str = ''):
    """Construct dataset from arguments

    We have two shuffle stage in the Dataset. The first is global
    shuffle at shards tar/raw file level. The second is global shuffle
    at training samples level.

    Args:
        data_list_file (str): Path to the file containing the list of data files.
        data_pipeline (callable): A function that applies the data pipeline to the input data.
        mode (str, optional): The mode of the dataset ('train', 'val', or 'test'). Defaults to 'train'.
        gan (bool, optional): Whether the dataset is for a GAN model. Defaults to False.
        shuffle (bool, optional): Whether to shuffle the dataset. Defaults to True.
        partition (bool, optional): Whether to partition the dataset based on the rank. Defaults to True.
        tts_file (str, optional): Path to the TTS file. Defaults to ''.
        prompt_utt2data (str, optional): Path to the prompt-utterance to data mapping file. Defaults to ''.
    """
    # Load the data file list
    with open(data_list_file, 'r') as f:
        data_files = [line.strip() for line in f.readlines()]

    # Shuffle the data files
    if shuffle:
        random.shuffle(data_files)

    # Partition the data files based on the rank
    if partition:
        rank = 0  # Assuming you have a way to get the current rank
        num_ranks = 1  # Assuming you have a way to get the total number of ranks
        data_files = [data_file for i, data_file in enumerate(data_files) if i % num_ranks == rank]

    # Create the dataset
    dataset = CustomDataset(data_files, data_pipeline, mode, gan, tts_file, prompt_utt2data)

    return dataset

class CustomDataset(Dataset):
    def __init__(self, data_files: List[str], data_pipeline: callable, mode: str, gan: bool, tts_file: str, prompt_utt2data: str):
        self.data_files = data_files
        self.data_pipeline = data_pipeline
        self.mode = mode
        self.gan = gan
        self.tts_file = tts_file
        self.prompt_utt2data = prompt_utt2data

    def __len__(self):
        return sum(1 for _ in self.data_files)

    def __getitem__(self, index):
        data_file = self.data_files[index]
        # Load and process the data using the data_pipeline
        data = self.data_pipeline(data_file)
        return data
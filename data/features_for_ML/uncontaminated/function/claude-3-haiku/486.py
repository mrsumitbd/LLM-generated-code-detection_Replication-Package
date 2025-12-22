import os
import pandas as pd

def get_predictions_from_file(predictions_path: str, dataset_name: str, split: str):
    """
    Loads predictions from a file and returns them as a pandas DataFrame.

    Args:
        predictions_path (str): The path to the file containing the predictions.
        dataset_name (str): The name of the dataset.
        split (str): The split of the dataset (e.g., 'train', 'val', 'test').

    Returns:
        pandas.DataFrame: A DataFrame containing the predictions.
    """
    file_path = os.path.join(predictions_path, f"{dataset_name}_{split}_predictions.csv")
    if os.path.exists(file_path):
        predictions = pd.read_csv(file_path)
        return predictions
    else:
        raise FileNotFoundError(f"Predictions file not found at {file_path}")
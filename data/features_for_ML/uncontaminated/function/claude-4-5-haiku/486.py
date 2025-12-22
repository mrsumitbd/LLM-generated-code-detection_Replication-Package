import json
import os
from pathlib import Path


def get_predictions_from_file(predictions_path: str, dataset_name: str, split: str):
    """
    Load predictions from a file based on dataset name and split.
    
    Args:
        predictions_path: Path to the predictions directory or file
        dataset_name: Name of the dataset
        split: Name of the split (e.g., 'train', 'test', 'validation')
    
    Returns:
        Predictions data (typically a list or dict)
    """
    # Handle both directory and file paths
    if os.path.isdir(predictions_path):
        # Try common naming patterns for prediction files
        possible_names = [
            f"{dataset_name}_{split}.json",
            f"{dataset_name}_{split}.jsonl",
            f"{split}.json",
            f"{split}.jsonl",
            f"{dataset_name}.json",
            f"{dataset_name}.jsonl",
        ]
        
        file_path = None
        for name in possible_names:
            candidate = os.path.join(predictions_path, name)
            if os.path.exists(candidate):
                file_path = candidate
                break
        
        if file_path is None:
            # List available files for debugging
            available_files = os.listdir(predictions_path)
            raise FileNotFoundError(
                f"No prediction file found for dataset '{dataset_name}' and split '{split}' in {predictions_path}. "
                f"Available files: {available_files}"
            )
    else:
        file_path = predictions_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prediction file not found: {file_path}")
    
    # Load the file based on extension
    if file_path.endswith('.jsonl'):
        predictions = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    predictions.append(json.loads(line))
        return predictions
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        # Try to load as JSON anyway
        with open(file_path, 'r') as f:
            content = f.read()
            # Try JSONL format first
            try:
                predictions = []
                for line in content.strip().split('\n'):
                    if line.strip():
                        predictions.append(json.loads(line))
                return predictions
            except json.JSONDecodeError:
                # Try regular JSON
                return json.loads(content)
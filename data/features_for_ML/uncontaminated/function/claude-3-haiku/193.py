import os
import pickle

def extract_and_store_features(dataset, model, repo):
    """
    Extracts features from the given dataset using the provided model and stores them in the specified repository.

    Args:
        dataset (pandas.DataFrame): The dataset to extract features from.
        model (object): The model to use for feature extraction.
        repo (str): The path to the repository where the extracted features will be stored.

    Returns:
        None
    """
    if not os.path.exists(repo):
        os.makedirs(repo)

    for i, row in dataset.iterrows():
        feature_vector = model.extract_features(row)
        feature_file = os.path.join(repo, f"feature_{i}.pkl")
        with open(feature_file, "wb") as f:
            pickle.dump(feature_vector, f)
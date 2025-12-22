import os
import json
import logging
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump, load

def feat_training_for_one_split(
    split: str,
    use_corpus: bool,
    use_matrix_input: bool,
    use_pretrained_model: bool,
    cfg,
    verbose=True,
):
    """
    Train a simple feature extractor / classifier for a single data split.

    Parameters
    ----------
    split : str
        Identifier of the split (e.g., 'train', 'valid', 'test').
    use_corpus : bool
        If True, load raw text data from cfg['text_path'][split] and vectorize with TF‑IDF.
    use_matrix_input : bool
        If True, load a pre‑computed numeric matrix from cfg['matrix_path'][split].
    use_pretrained_model : bool
        If True, load a pretrained LogisticRegression model from cfg['pretrained_path'].
    cfg : dict
        Configuration dictionary containing paths and hyperparameters.
    verbose : bool, default=True
        If True, print progress messages.

    Returns
    -------
    model : sklearn.base.BaseEstimator
        Trained (or loaded) model.
    X_train : np.ndarray
        Feature matrix used for training.
    y_train : np.ndarray
        Labels used for training.
    """
    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    if use_corpus:
        text_path = cfg.get("text_path", {}).get(split)
        if not text_path or not os.path.exists(text_path):
            raise FileNotFoundError(f"Text file for split '{split}' not found at {text_path}")
        df = pd.read_csv(text_path)
        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("CSV must contain 'text' and 'label' columns")
        X_raw = df["text"].astype(str).tolist()
        y = df["label"].values
        if verbose:
            logger.info(f"Loaded {len(X_raw)} text samples from {text_path}")
        # Vectorize
        vectorizer = TfidfVectorizer(
            max_features=cfg.get("max_features", 5000),
            ngram_range=tuple(cfg.get("ngram_range", (1, 1))),
        )
        X = vectorizer.fit_transform(X_raw)
        if verbose:
            logger.info(f"TF‑IDF vectorized to shape {X.shape}")
    elif use_matrix_input:
        matrix_path = cfg.get("matrix_path", {}).get(split)
        if not matrix_path or not os.path.exists(matrix_path):
            raise FileNotFoundError(f"Matrix file for split '{split}' not found at {matrix_path}")
        X = np.load(matrix_path)
        label_path = cfg.get("label_path", {}).get(split)
        if not label_path or not os.path.exists(label_path):
            raise FileNotFoundError(f"Label file for split '{split}' not found at {label_path}")
        y = np.load(label_path)
        if verbose:
            logger.info(f"Loaded matrix of shape {X.shape} and labels of shape {y.shape}")
    else:
        raise ValueError("Either use_corpus or use_matrix_input must be True")

    # ------------------------------------------------------------------
    # 2. Train / load model
    # ------------------------------------------------------------------
    if use_pretrained_model:
        pretrained_path = cfg.get("pretrained_path")
        if not pretrained_path or not os.path.exists(pretrained_path):
            raise FileNotFoundError(f"Pretrained model not found at {pretrained_path}")
        model = load(pretrained_path)
        if verbose:
            logger.info(f"Loaded pretrained model from {pretrained_path}")
    else:
        # Split into train/validation for quick sanity check
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=cfg.get("random_state", 42)
        )
        model = LogisticRegression(
            max_iter=cfg.get("max_iter", 1000),
            C=cfg.get("C", 1.0),
            solver=cfg.get("solver", "lbfgs"),
        )
        model.fit(X_train, y_train)
        if verbose:
            preds = model.predict(X_val)
            acc = accuracy_score(y_val, preds)
            logger.info(f"Trained model; validation accuracy: {acc:.4f}")

    # ------------------------------------------------------------------
    # 3. Return
    # ------------------------------------------------------------------
    return model, X, y
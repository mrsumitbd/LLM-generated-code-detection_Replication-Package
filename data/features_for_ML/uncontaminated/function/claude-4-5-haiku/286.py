def feat_training_for_one_split(
    split: str,
    use_corpus: bool,
    use_matrix_input: bool,
    use_pretrained_model: bool,
    cfg,
    verbose=True,
):
    import os
    import numpy as np
    from pathlib import Path
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Training features for split: {split}")
        print(f"{'='*60}")
    
    # Initialize data structures
    features_dict = {}
    metadata = {
        'split': split,
        'use_corpus': use_corpus,
        'use_matrix_input': use_matrix_input,
        'use_pretrained_model': use_pretrained_model,
    }
    
    # Load or prepare data based on configuration
    if use_corpus:
        if verbose:
            print(f"Loading corpus data for {split}...")
        # Load corpus data
        corpus_data = _load_corpus_data(split, cfg)
    else:
        corpus_data = None
    
    if use_matrix_input:
        if verbose:
            print(f"Loading matrix input for {split}...")
        # Load matrix input
        matrix_data = _load_matrix_data(split, cfg)
    else:
        matrix_data = None
    
    if use_pretrained_model:
        if verbose:
            print(f"Loading pretrained model...")
        # Load pretrained model
        model = _load_pretrained_model(cfg)
    else:
        model = None
    
    # Extract features
    if verbose:
        print(f"Extracting features...")
    
    if corpus_data is not None:
        features_dict['corpus_features'] = _extract_corpus_features(
            corpus_data, cfg
        )
    
    if matrix_data is not None:
        features_dict['matrix_features'] = _extract_matrix_features(
            matrix_data, cfg
        )
    
    if model is not None:
        features_dict['model_features'] = _extract_model_features(
            corpus_data or matrix_data, model, cfg
        )
    
    # Combine features
    if verbose:
        print(f"Combining features...")
    
    combined_features = _combine_features(features_dict, cfg)
    
    # Save results
    if verbose:
        print(f"Saving results...")
    
    output_path = _get_output_path(split, cfg)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    _save_features(combined_features, metadata, output_path, cfg)
    
    if verbose:
        print(f"Training completed for split: {split}")
        print(f"Results saved to: {output_path}")
    
    return {
        'features': combined_features,
        'metadata': metadata,
        'output_path': output_path,
    }


def _load_corpus_data(split: str, cfg):
    """Load corpus data for the given split."""
    corpus_path = getattr(cfg, 'corpus_path', None)
    if corpus_path:
        import pickle
        file_path = os.path.join(corpus_path, f"{split}.pkl")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
    return None


def _load_matrix_data(split: str, cfg):
    """Load matrix data for the given split."""
    matrix_path = getattr(cfg, 'matrix_path', None)
    if matrix_path:
        import numpy as np
        file_path = os.path.join(matrix_path, f"{split}.npy")
        if os.path.exists(file_path):
            return np.load(file_path)
    return None


def _load_pretrained_model(cfg):
    """Load pretrained model."""
    model_path = getattr(cfg, 'pretrained_model_path', None)
    if model_path and os.path.exists(model_path):
        import pickle
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None


def _extract_corpus_features(corpus_data, cfg):
    """Extract features from corpus data."""
    if corpus_data is None:
        return None
    return {'corpus': corpus_data}


def _extract_matrix_features(matrix_data, cfg):
    """Extract features from matrix data."""
    if matrix_data is None:
        return None
    return {'matrix': matrix_data}


def _extract_model_features(data, model, cfg):
    """Extract features using pretrained model."""
    if model is None or data is None:
        return None
    return {'model': model}


def _combine_features(features_dict, cfg):
    """Combine multiple feature sources."""
    combined = {}
    for key, value in features_dict.items():
        if value is not None:
            combined.update(value)
    return combined


def _get_output_path(split: str, cfg):
    """Get output path for features."""
    output_dir = getattr(cfg, 'output_dir', './output')
    return os.path.join(output_dir, f"features_{split}.pkl")


def _save_features(features, metadata, output_path, cfg):
    """Save features to disk."""
    import pickle
    data = {'features': features, 'metadata': metadata}
    with open(output_path, 'wb') as f:
        pickle.dump(data, f)
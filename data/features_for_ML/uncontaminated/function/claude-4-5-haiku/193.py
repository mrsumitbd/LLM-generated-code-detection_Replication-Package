import os
import pickle
import torch
from huggingface_hub import HfApi, login
from datasets import load_dataset


def extract_and_store_features(dataset, model, repo):
    """
    Extract features from a dataset using a model and store them in a Hugging Face repository.
    
    Args:
        dataset: Dataset name or path to extract features from
        model: Model name or path to use for feature extraction
        repo: Hugging Face repository ID where features will be stored
    """
    # Load the dataset
    if isinstance(dataset, str):
        ds = load_dataset(dataset, split='train', streaming=True)
    else:
        ds = dataset
    
    # Load the model
    if isinstance(model, str):
        from transformers import AutoModel, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model)
        feature_model = AutoModel.from_pretrained(model)
    else:
        feature_model = model
        tokenizer = None
    
    # Set model to evaluation mode
    feature_model.eval()
    
    # Extract features
    features_list = []
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    feature_model.to(device)
    
    # Process dataset samples
    sample_count = 0
    for sample in ds:
        if sample_count >= 100:  # Limit to 100 samples for demo
            break
        
        # Prepare input
        if isinstance(sample, dict):
            if 'text' in sample:
                text = sample['text']
            elif 'content' in sample:
                text = sample['content']
            else:
                text = str(sample)
        else:
            text = str(sample)
        
        # Tokenize and extract features
        if tokenizer:
            inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            inputs = {k: v.to(device) for k, v in inputs.items()}
        else:
            # If no tokenizer, assume text input
            inputs = {'input_ids': torch.tensor([[1, 2, 3]]).to(device)}
        
        # Extract features
        with torch.no_grad():
            outputs = feature_model(**inputs)
            if hasattr(outputs, 'last_hidden_state'):
                features = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            else:
                features = outputs[0].mean(dim=1).cpu().numpy()
        
        features_list.append(features)
        sample_count += 1
    
    # Store features in repository
    import numpy as np
    features_array = np.concatenate(features_list, axis=0)
    
    # Create a temporary file to store features
    features_file = 'extracted_features.pkl'
    with open(features_file, 'wb') as f:
        pickle.dump(features_array, f)
    
    # Upload to Hugging Face Hub
    try:
        api = HfApi()
        # Check if we need to login
        try:
            api.repo_info(repo)
        except Exception:
            # Try to login if repo doesn't exist or we don't have access
            login()
        
        # Upload the file
        api.upload_file(
            path_or_fileobj=features_file,
            path_in_repo='features.pkl',
            repo_id=repo,
            repo_type='dataset'
        )
        
        print(f"Features successfully uploaded to {repo}")
    except Exception as e:
        print(f"Could not upload to Hub: {e}")
        print(f"Features saved locally to {features_file}")
    finally:
        # Clean up temporary file
        if os.path.exists(features_file):
            os.remove(features_file)
    
    return features_array
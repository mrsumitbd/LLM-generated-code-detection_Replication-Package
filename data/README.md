# Data Directory

This directory contains all datasets, features, and trained models used in the paper.

## Directory Structure
```
data/
├── LLM_generated_contents_intersection/     # Generated code samples (intersection dataset)
├── features_for_ML/                         # Extracted features for machine learning
├── trained_ML_models/                       # Trained CatBoost models (.pkl files)
├── data_for_ML_validation/                  # Test data splits
├── uncontaminated_intersection_keys_class.txt
└── uncontaminated_intersection_keys_function.txt
```

## Dataset Description

### LLM_generated_contents_intersection/
Contains LLM-generated code samples filtered to the **global intersection** of all four models:
- `claude-3-haiku_class_level_filtered.csv` (131 MB)
- `claude-3-haiku_func_level_filtered.csv` (48 MB)
- `claude-4_5-haiku_class_level_filtered.csv` (162 MB)
- `claude-4_5-haiku_func_level_filtered.csv` (56 MB)
- `gpt-3_5_class_level_filtered.csv` (110 MB)
- `gpt-3_5_func_level_filtered.csv` (34 MB)
- `gpt-oss_class_level_filtered.csv` (167 MB)
- `gpt-oss_func_level_filtered.csv` (69 MB)
- `common_ids_class_level.csv` (2.0 MB) - IDs in the intersection
- `common_ids_func_level.csv` (870 KB) - IDs in the intersection

**Format:** Each CSV contains columns: `id`, `human_code`, `llm_generated_code`, `metadata`

### features_for_ML/
Extracted features organized by granularity:

#### class_global_intersection/
Features for class-level code across all models:
- `claude-3-haiku/` - Claude 3 Haiku generated classes
- `claude-4-5-haiku/` - Claude 4.5 Haiku generated classes  
- `gpt-3-5/` - GPT-3.5 generated classes
- `gpt-oss/` - GPT-OSS generated classes
- `human/` - Human-written classes (from CodeSearchNet)

#### function_global_intersection/
Features for function-level code across all models (same structure as above)

#### uncontaminated/
Features for validation on contamination-free data:
- `class/` - Uncontaminated class-level features
- `function/` - Uncontaminated function-level features

**Feature Files:** Each subdirectory contains CSV files with 57 extracted metrics:
- 18 stylometry features (e.g., avg_line_length, comment_ratio)
- 30 complexity features (e.g., cyclomatic_complexity, nesting_depth)
- Additional structural metrics

### trained_ML_models/
Pre-trained CatBoost models (8 configurations: 4 models × 2 granularities):
- `class_claude-3-haiku_finalized_model_intersection.pkl`
- `class_claude-4-5-haiku_finalized_model_intersection.pkl`
- `class_gpt-3-5_finalized_model_intersection.pkl`
- `class_gpt-oss_finalized_model_intersection.pkl`
- `function_claude-3-haiku_finalized_model_intersection.pkl`
- `function_claude-4-5-haiku_finalized_model_intersection.pkl`
- `function_gpt-3-5_finalized_model_intersection.pkl`
- `function_gpt-oss_finalized_model_intersection.pkl`

**Model Details:**
- Algorithm: CatBoost Classifier
- Training: 80/20 train-test split with stratification
- Hyperparameters: Optimized using grid search with 5-fold cross-validation
- Size: ~1.1 MB per model

### data_for_ML_validation/
Test set splits for model evaluation (intersection dataset only):
- 8 files: `{model}_{granularity}_test_data_intersection.csv`
- Contains held-out 20% of data for performance evaluation
- Used to generate results in `results/model_performance_*.csv`

### Uncontaminated Validation Keys
- `uncontaminated_intersection_keys_class.txt` (46 KB) - 1,000 class IDs from post-2024 repositories
- `uncontaminated_intersection_keys_function.txt` (69 KB) - 1,500 function IDs from post-2024 repositories

These IDs reference code samples that were:
1. Created after the LLM training cutoff dates
2. Extracted from repositories created after 2024-01-01
3. Used for contamination-free validation (see `results/uncontaminated_validation_results.csv`)

## Data Provenance

**Source:** CodeSearchNet dataset (Python subset)
- Original repository: https://github.com/github/CodeSearchNet
- Filtering: Intersection methodology ensures all four models generated code for the same human-written samples
- License: Original CodeSearchNet license applies

**LLM Generation:**
- Models: Claude 3 Haiku, Claude 4.5 Haiku, GPT-3.5-turbo, GPT-OSS (via Together AI)
- Prompt template: "Generate Python code for: {docstring}"
- Temperature: 0.7 for all models
- Generation scripts: See `src/batch_generate_*.py`

## Usage

### Loading Generated Code
```python
import pandas as pd

# Load intersection dataset for a specific model
claude_classes = pd.read_csv('LLM_generated_contents_intersection/claude-3-haiku_class_level_filtered.csv')
print(f"Samples: {len(claude_classes)}")
```

### Loading Features
```python
# Load features for training
import os
feature_dir = 'features_for_ML/function_global_intersection/claude-3-haiku/'
feature_files = [f for f in os.listdir(feature_dir) if f.endswith('.csv')]
# Each file contains features for a batch of samples
```

### Loading Pre-trained Models
```python
import pickle

# Load a trained model
with open('trained_ML_models/function_claude-3-haiku_finalized_model_intersection.pkl', 'rb') as f:
    model = pickle.load(f)

# Model is ready for prediction
# predictions = model.predict(X_test)
```

## Data Statistics

**Intersection Dataset Size:**
- Function-level: ~15,000 samples per model
- Class-level: ~10,000 samples per model

**Train/Test Split:**
- Training: 80% of intersection data
- Testing: 20% of intersection data
- Stratified by label (human vs. LLM-generated)

**Uncontaminated Validation:**
- Classes: 1,000 samples
- Functions: 1,500 samples
- Post-2024 repositories only

## Notes

- All data uses the **global intersection methodology** described in the paper
- Non-intersection datasets have been excluded from this replication package
- Feature extraction performed using SciTools Understand™ (commercial tool required for regeneration)
- Trained models can be used directly without Understand™

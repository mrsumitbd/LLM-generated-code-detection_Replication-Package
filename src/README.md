# Source Code Documentation

This directory contains all scripts for data generation, feature extraction, model training, and analysis.

## Pipeline Overview
```
1. Code Generation → 2. Feature Extraction → 3. Model Training → 4. RQ Analysis
   (batch_*.py)        (prepare_for_understand.py)  (model_training.py)   (rq*.py)
```

## Scripts by Function

### 1. Code Generation Scripts

#### `batch_generate_with_anthropicai.py`
Generates code using Anthropic's Claude models (Claude 3 Haiku, Claude 4.5 Haiku).

**Usage:**
```bash
python batch_generate_with_anthropicai.py \
    --model claude-3-haiku \
    --granularity function \
    --input data/codesearchnet_python.csv \
    --output data/LLM_generated_contents/
```

**Arguments:**
- `--model`: Model name (`claude-3-haiku`, `claude-4-5-haiku`)
- `--granularity`: Code granularity (`function`, `class`)
- `--input`: Path to CodeSearchNet input file
- `--output`: Output directory for generated code
- `--batch-size`: Batch size for API calls (default: 100)
- `--temperature`: Sampling temperature (default: 0.7)

**Requirements:**
- Anthropic API key set in environment: `ANTHROPIC_API_KEY`
- Input CSV with columns: `id`, `docstring`, `code`

**Output:**
- CSV file: `{model}_{granularity}_level_filtered.csv`
- Columns: `id`, `human_code`, `llm_generated_code`, `metadata`

#### `batch_generation_with_openai.py`
Generates code using OpenAI's GPT models (GPT-3.5-turbo).

**Usage:**
```bash
python batch_generation_with_openai.py \
    --model gpt-3.5-turbo \
    --granularity function \
    --input data/codesearchnet_python.csv \
    --output data/LLM_generated_contents/
```

**Arguments:** Same as `batch_generate_with_anthropicai.py`

**Requirements:**
- OpenAI API key: `OPENAI_API_KEY`

#### `generation_with_togetherai.py`
Generates code using Together AI models (GPT-OSS).

**Usage:**
```bash
python generation_with_togetherai.py \
    --model gpt-oss \
    --granularity function \
    --input data/codesearchnet_python.csv \
    --output data/LLM_generated_contents/
```

**Requirements:**
- Together AI API key: `TOGETHER_API_KEY`

---

### 2. Feature Extraction

#### `prepare_for_understand.py`
Prepares generated code for metric extraction using SciTools Understand™.

**Usage:**
```bash
python prepare_for_understand.py \
    --granularity function \
    --model claude-3-haiku \
    --input data/LLM_generated_contents_intersection/ \
    --output data/Code_for_Understand_analysis/
```

**Process:**
1. Reads LLM-generated code CSV
2. Writes individual `.py` files for each sample
3. Creates Understand-compatible project structure
4. Generates batch processing scripts

**Output:**
- Individual Python files: `{id}.py`
- Project directory ready for Understand analysis
- Metadata mapping: `id_to_file_mapping.csv`

**Next Step:**
Run SciTools Understand™ to extract metrics:
- Open Understand™
- Create new project with generated `.py` files
- Export metrics to CSV (57 metrics per file)
- Save to `data/features_for_ML/{granularity}_global_intersection/{model}/`

---

### 3. Model Training

#### `model_training.py`
Trains CatBoost classifiers for LLM-generated code detection.

**Usage:**
```bash
python model_training.py \
    --model claude-3-haiku \
    --granularity function \
    --features data/features_for_ML/function_global_intersection/ \
    --output data/trained_ML_models/
```

**Arguments:**
- `--model`: LLM model name
- `--granularity`: Code granularity (`function`, `class`)
- `--features`: Path to feature directory
- `--output`: Output directory for trained models
- `--test-size`: Test split ratio (default: 0.2)
- `--cv-folds`: Cross-validation folds (default: 5)

**Process:**
1. Loads features for human and LLM-generated code
2. Merges into single dataset with labels (0=human, 1=LLM)
3. Splits into 80/20 train/test (stratified)
4. Grid search hyperparameter tuning with 5-fold CV
5. Trains final model on full training set
6. Evaluates on test set
7. Saves model and test data

**Hyperparameters Tuned:**
- `iterations`: [100, 200, 300]
- `depth`: [4, 6, 8]
- `learning_rate`: [0.01, 0.03, 0.1]

**Output:**
- Trained model: `{granularity}_{model}_finalized_model_intersection.pkl`
- Test data: `{model}_{granularity}_test_data_intersection.csv`
- Performance metrics: `model_performance_{granularity}_{model}_intersection.csv`
- Bootstrap CI: `bootstrap_results_{granularity}_{model}_intersection.csv`
- Selected features: `selected_features_{granularity}_{model}_intersection.csv`

---

### 4. RQ Analysis Scripts

#### `rq1_statistical_analysis.py`
Statistical analysis of feature distributions (RQ1).

**Usage:**
```bash
python rq1_statistical_analysis.py
```

**Process:**
1. Loads features for human and LLM code (8 configurations)
2. Computes Mann-Whitney U test for each feature
3. Applies Holm-Bonferroni correction (α=0.01)
4. Calculates effect sizes (Cliff's Delta)
5. Categorizes divergence direction (upward/downward)

**Output:**
- `results/rq1_statistical_results_detailed_intersection.csv`
  - Columns: model, granularity, feature, U_statistic, p_value, effect_size, significant, direction
- `results/rq1_summary_counts_intersection.csv`
  - Summary: significant_features_up, significant_features_down, large_effects

**Key Findings:**
- Claude 3 Haiku: Moderate downward divergence
- GPT-3.5: Extreme downward divergence with large effects
- GPT-OSS: Consistent upward divergence

#### `rq2_delong_test.py`
DeLong test for comparing ROC curves (RQ2).

**Usage:**
```bash
python rq2_delong_test.py
```

**Process:**
1. Loads test data and predictions for all 8 configurations
2. Computes ROC curves and AUC for each
3. Performs pairwise DeLong tests
4. Reports p-values and confidence intervals

**Output:**
- `results/delong_test_results_intersection.csv`
  - Columns: model1, model2, granularity, auc1, auc2, p_value, significant

**Statistical Method:**
- DeLong test for correlated ROC curves
- Bonferroni correction for multiple comparisons
- α=0.05

#### `rq3_feature_overlap_analysis.py`
Feature importance overlap analysis (RQ3).

**Usage:**
```bash
python rq3_feature_overlap_analysis.py
```

**Process:**
1. Loads SHAP values for all 8 configurations
2. Ranks features by mean absolute SHAP
3. Selects top-10 features per configuration
4. Computes Jaccard similarity between models
5. Analyzes overlap patterns

**Output:**
- `results/rq3_summary_statistics_intersection.csv`
  - Mean/median features, total unique features
- `results/rq3_function_jaccard_matrix_intersection.csv`
  - Pairwise Jaccard similarity (functions)
- `results/rq3_class_jaccard_matrix_intersection.csv`
  - Pairwise Jaccard similarity (classes)
- `results/rq3_feature_frequency_intersection.csv`
  - How often each feature appears in top-10
- `results/rq3_granularity_overlap_intersection.csv`
  - Overlap between function and class granularities

**Figures:**
- `figures/rq3_feature_frequency_intersection.pdf`
- `figures/rq3_feature_overlap_heatmaps_intersection.pdf`

#### `shap_analysis.py`
SHAP value computation and visualization.

**Usage:**
```bash
python shap_analysis.py
```

**Process:**
1. Loads trained models and test data (8 configurations)
2. Computes SHAP values using TreeExplainer
3. Runs Scott-Knott ESD ranking
4. Generates beeswarm plots and ranking visualizations

**Output:**
- `results/shap_values_all_configs_intersection.csv`
  - All SHAP values for all samples
- `results/feature_importance_summary_intersection.csv`
  - Mean absolute SHAP per feature
- `results/feature_rankings_all_configs_intersection.csv`
  - Scott-Knott ESD ranks
- `figures/{model}_{granularity}_catboost_shap_beeswarm_intersection.pdf`
  - SHAP beeswarm plots (8 files)
- `figures/{granularity}_{model}_ranking.pdf`
  - Scott-Knott ranking plots (8 files)

**Visualization Features:**
- Beeswarm: Feature values vs. SHAP impact
- Rankings: Scott-Knott groups with statistical significance

---

### 5. Validation Scripts

#### `prediction_on_uncontaminated_data.py`
Validates models on contamination-free post-2024 data.

**Usage:**
```bash
python prediction_on_uncontaminated_data.py
```

**Process:**
1. Loads uncontaminated intersection keys
2. Extracts corresponding features
3. Loads trained models
4. Makes predictions
5. Computes performance metrics

**Output:**
- `results/uncontaminated_validation_results.csv`
  - Columns: model, granularity, accuracy, precision, recall, f1, auc_roc

**Purpose:**
- Verify models generalize to post-training data
- Confirm no data contamination issues

#### `uncontaminated_intersection_analysis.py`
Analyzes intersection properties of uncontaminated data.

**Usage:**
```bash
python uncontaminated_intersection_analysis.py
```

**Process:**
1. Identifies common IDs across all four models
2. Extracts post-2024 repository samples
3. Generates intersection keys
4. Validates against training data

**Output:**
- `data/uncontaminated_intersection_keys_function.txt`
- `data/uncontaminated_intersection_keys_class.txt`

---

### 6. Utility Functions

#### `utility.py`
Common helper functions used across scripts.

**Key Functions:**
```python
def load_features(feature_dir, model, granularity):
    """Load and merge feature CSV files."""
    
def compute_intersection(id_lists):
    """Compute global intersection of sample IDs."""
    
def apply_feature_selection(X, y, method='mutual_info'):
    """Select top-k features using mutual information."""
    
def bootstrap_confidence_interval(y_true, y_pred, metric='accuracy', n_bootstrap=1000):
    """Compute bootstrap CI for performance metrics."""
    
def plot_confusion_matrix(y_true, y_pred, labels, output_path):
    """Generate and save confusion matrix plot."""
```

---

## Execution Order

### Full Pipeline (from scratch)
```bash
# 1. Generate code (requires API keys)
python batch_generate_with_anthropicai.py --model claude-3-haiku --granularity function
python batch_generate_with_anthropicai.py --model claude-4-5-haiku --granularity function
python batch_generation_with_openai.py --model gpt-3.5-turbo --granularity function
python generation_with_togetherai.py --model gpt-oss --granularity function

# Repeat for class-level
# ... (4 more commands)

# 2. Prepare for feature extraction
python prepare_for_understand.py --granularity function --model claude-3-haiku
# ... (7 more commands for other configs)

# 3. Extract features using Understand™ (manual step)
# Open Understand, create projects, export metrics

# 4. Train models
python model_training.py --model claude-3-haiku --granularity function
# ... (7 more commands)

# 5. Run RQ analyses
python rq1_statistical_analysis.py
python rq2_delong_test.py
python rq3_feature_overlap_analysis.py
python shap_analysis.py

# 6. Validation
python prediction_on_uncontaminated_data.py
```

### Using Provided Data (recommended)
```bash
# Models and features already provided - just run analyses
python rq1_statistical_analysis.py
python rq2_delong_test.py
python rq3_feature_overlap_analysis.py
python shap_analysis.py
python prediction_on_uncontaminated_data.py
```

---

## Configuration

### Environment Variables Required
```bash
# For code generation (if regenerating data)
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export TOGETHER_API_KEY="your-key-here"

# For Understand™ (if extracting features)
export UNDERSTAND_LICENSE="your-license-here"
```

### Common Parameters

**Models:** `claude-3-haiku`, `claude-4-5-haiku`, `gpt-3.5-turbo`, `gpt-oss`  
**Granularities:** `function`, `class`  
**Train/Test Split:** 80/20 (stratified)  
**Cross-Validation:** 5-fold  
**Statistical Threshold:** α=0.01 (Holm-Bonferroni corrected)  
**Bootstrap Iterations:** 1,000  

---

## Troubleshooting

### Memory Issues
- Reduce batch size in generation scripts
- Process models sequentially instead of parallel
- Use `--low-memory` flag if available

### API Rate Limits
- Increase sleep time between batches
- Use exponential backoff
- Check API usage quotas

### Understand™ Not Found
- Verify installation path
- Set `UNDERSTAND_BIN` environment variable
- Use pre-extracted features instead

### Missing Dependencies
```bash
pip install -r ../requirements.txt
```

---

## Performance Notes

**Typical Execution Times (on 16GB RAM, 8-core CPU):**
- Code generation (1 model, 1 granularity): 2-4 hours
- Feature extraction (Understand™): 1-2 hours
- Model training (1 configuration): 10-20 minutes
- RQ1 analysis: 5 minutes
- RQ2 analysis: 2 minutes
- RQ3 analysis: 10 minutes
- SHAP analysis: 15-30 minutes

**Total:** ~8-12 hours for full pipeline (or ~1 hour using provided data)

---

## Contact

For script-specific questions or issues, please refer to inline documentation or contact [your email].

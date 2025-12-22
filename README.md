# Replication Package: Detecting LLM-Generated Code

This repository contains the complete replication package for our paper on detecting LLM-generated code across multiple models and granularities.

## Paper Information

**Title:** [Your Paper Title]  
**Authors:** [Your Names]  
**Venue:** [Submitted to TOSEM/EMSE]  
**Year:** 2025

## Overview

This replication package enables full reproduction of our experimental results, including:
- Statistical analysis of feature distributions (RQ1)
- Model performance evaluation with DeLong tests (RQ2)  
- Feature importance and overlap analysis (RQ3)
- Validation on contamination-free datasets

## Repository Structure
```
.
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── data/                        # Datasets and trained models
│   ├── LLM_generated_contents_intersection/
│   ├── features_for_ML/
│   ├── trained_ML_models/
│   ├── data_for_ML_validation/
│   └── README.md
├── src/                         # Source code
│   ├── batch_generate_*.py      # Code generation scripts
│   ├── prepare_for_understand.py
│   ├── model_training.py
│   ├── rq1_statistical_analysis.py
│   ├── rq2_delong_test.py
│   ├── rq3_feature_overlap_analysis.py
│   ├── shap_analysis.py
│   └── utility.py
├── results/                     # Experimental results (CSV)
└── figures/                     # Publication figures (PDF)
```

## Quick Start

### Prerequisites

- Python 3.8+
- 16GB+ RAM recommended
- SciTools Understand™ (for feature extraction only - not needed if using provided features)

### Installation
```bash
# Clone the repository
git clone [your-repo-url]
cd LLM-generated-code-detection_Replication-Package

# Install dependencies
pip install -r requirements.txt
```

### Using Pre-trained Models
```python
import pickle
import pandas as pd

# Load a trained model
with open('data/trained_ML_models/function_claude-3-haiku_finalized_model_intersection.pkl', 'rb') as f:
    model = pickle.load(f)

# Load test data
test_data = pd.read_csv('data/data_for_ML_validation/claude-3-haiku_function_test_data_intersection.csv')
X_test = test_data.drop(['label', 'id'], axis=1)
y_test = test_data['label']

# Make predictions
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)
```

## Research Questions

### RQ1: Feature Distribution Analysis
**Question:** How do feature distributions differ between human-written and LLM-generated code?

**Script:** `src/rq1_statistical_analysis.py`  
**Results:** `results/rq1_statistical_results_detailed_intersection.csv`  
**Figures:** N/A (results presented in tables)

**Key Findings:**
- Claude 3 Haiku: Moderate downward divergence (3 function, 23 class features)
- Claude 4.5 Haiku: Mixed pattern (13↑ function, 2↑ class, 1↓ function)
- GPT-3.5: Extreme downward divergence (17 function, 29 class features)
- GPT-OSS: Consistent upward divergence (18 function, 9 class features)

**Statistical Method:** Mann-Whitney U test with Holm-Bonferroni correction (α=0.01)

### RQ2: Detection Performance
**Question:** How accurately can we detect LLM-generated code?

**Scripts:** 
- `src/model_training.py` - Train CatBoost models
- `src/rq2_delong_test.py` - Statistical comparison of ROC curves

**Results:** 
- `results/model_performance_*_intersection.csv` (8 files)
- `results/delong_test_results_intersection.csv`
- `results/uncontaminated_validation_results.csv`

**Figures:**
- `figures/rq2_confusion_matrices.pdf`
- `figures/rq2_roc_curves.pdf`

**Key Findings:**
- AUC-ROC: 0.85-0.95 across all configurations
- F1-Score: 0.80-0.92
- DeLong test: Significant differences between model pairs (p < 0.001)
- Uncontaminated validation: Performance maintained on post-2024 data

### RQ3: Feature Importance and Overlap
**Question:** Which features are most important, and do they overlap across models?

**Scripts:**
- `src/shap_analysis.py` - SHAP value computation
- `src/rq3_feature_overlap_analysis.py` - Jaccard similarity and overlap analysis

**Results:**
- `results/feature_importance_summary_intersection.csv`
- `results/feature_rankings_all_configs_intersection.csv`
- `results/shap_values_all_configs_intersection.csv`
- `results/rq3_*.csv` (5 files)

**Figures:**
- `figures/*_shap_beeswarm_intersection.pdf` (8 files)
- `figures/*_ranking.pdf` (8 files - Scott-Knott ESD rankings)
- `figures/rq3_feature_frequency_intersection.pdf`
- `figures/rq3_feature_overlap_heatmaps_intersection.pdf`
- `figures/feature_importance_heatmap_intersection.pdf`

**Key Findings:**
- Top features: cyclomatic_complexity, nesting_depth, avg_line_length
- Jaccard similarity: 0.45-0.65 between models (moderate overlap)
- Function-level: Higher overlap than class-level
- Scott-Knott ESD: 3-4 distinct groups of feature importance

## Reproducing Results

### Step 1: Generate Code (Optional - data provided)
```bash
# Generate code with Claude 3 Haiku
python src/batch_generate_with_anthropicai.py --model claude-3-haiku --granularity function

# Generate code with GPT-3.5
python src/batch_generation_with_openai.py --model gpt-3.5-turbo --granularity function

# Generate code with Together AI models
python src/generation_with_togetherai.py --model gpt-oss --granularity function
```

**Note:** Requires API keys for Anthropic, OpenAI, and Together AI.

### Step 2: Extract Features (Optional - features provided)
```bash
# Prepare data for Understand analysis
python src/prepare_for_understand.py --granularity function --model claude-3-haiku

# Run Understand™ to extract metrics (commercial tool required)
# Output: CSV files in data/features_for_ML/
```

**Note:** SciTools Understand™ license required. Pre-extracted features are provided.

### Step 3: Train Models (Optional - trained models provided)
```bash
# Train all 8 configurations (4 models × 2 granularities)
bash src/model_training.sh

# Or train a single configuration
python src/model_training.py --model claude-3-haiku --granularity function
```

**Output:** Trained models saved to `data/trained_ML_models/`

### Step 4: Reproduce RQ1 Results
```bash
python src/rq1_statistical_analysis.py
```

**Output:**
- `results/rq1_statistical_results_detailed_intersection.csv`
- `results/rq1_summary_counts_intersection.csv`

### Step 5: Reproduce RQ2 Results
```bash
# DeLong test for ROC curve comparison
python src/rq2_delong_test.py

# Validate on uncontaminated data
python src/prediction_on_uncontaminated_data.py
```

**Output:**
- `results/delong_test_results_intersection.csv`
- `results/uncontaminated_validation_results.csv`

### Step 6: Reproduce RQ3 Results
```bash
# Compute SHAP values
python src/shap_analysis.py

# Analyze feature overlap
python src/rq3_feature_overlap_analysis.py
```

**Output:**
- `results/shap_values_all_configs_intersection.csv`
- `results/feature_importance_summary_intersection.csv`
- `results/rq3_*.csv`
- `figures/*_shap_beeswarm_intersection.pdf`
- `figures/*_ranking.pdf`

## Key Features

### Global Intersection Methodology
All experiments use the **global intersection** of samples across all four LLMs:
- Ensures fair comparison (same human code samples)
- Eliminates bias from sample selection
- Reduces dataset size but increases validity

### Statistical Rigor
- Mann-Whitney U test with Holm-Bonferroni correction (RQ1)
- DeLong test for ROC curve comparison (RQ2)
- Bootstrap confidence intervals (95%)
- Effect size reporting (Cliff's Delta)

### Contamination-Free Validation
- Post-2024 repository extraction
- Validation on 1,000 classes and 1,500 functions
- Results in `results/uncontaminated_validation_results.csv`

### Interpretability
- SHAP values for feature importance
- Scott-Knott ESD for feature ranking
- Comprehensive visualizations

## Dependencies

Major dependencies (see `requirements.txt` for complete list):
- `catboost==1.2.2` - Gradient boosting classifier
- `shap==0.43.0` - SHAP value computation
- `scikit-learn==1.3.2` - Machine learning utilities
- `pandas==2.1.3` - Data manipulation
- `numpy==1.26.2` - Numerical computing
- `matplotlib==3.8.2` - Plotting
- `seaborn==0.13.0` - Statistical visualization
- `scipy==1.11.4` - Statistical tests

## Data Availability

### Included in Repository
- ✅ LLM-generated code (intersection dataset)
- ✅ Extracted features (57 metrics per sample)
- ✅ Trained models (8 configurations)
- ✅ Test data splits
- ✅ All experimental results (CSV)
- ✅ Publication figures (PDF)

### External Dependencies
- CodeSearchNet dataset (Python subset): https://github.com/github/CodeSearchNet
- SciTools Understand™ (for feature extraction): https://scitools.com/

## Citation

If you use this replication package, please cite our paper:
```bibtex
@article{yourpaper2025,
  title={[Your Paper Title]},
  author={[Your Names]},
  journal={[TOSEM/EMSE]},
  year={2025}
}
```

## License

[Specify license - e.g., MIT, Apache 2.0]

The original CodeSearchNet dataset is licensed under [original license].

## Contact

For questions or issues:
- **Primary Contact:** [Your Email]
- **Repository Issues:** [GitHub Issues URL]

## Acknowledgments

- CodeSearchNet dataset: GitHub and collaborators
- SciTools Understand™: SciTools, Inc.
- Compute resources: [Your institution/grant]

## Changelog

### v1.0.0 (2025-01-XX)
- Initial release for TOSEM/EMSE submission
- Complete replication package with all data, code, and results

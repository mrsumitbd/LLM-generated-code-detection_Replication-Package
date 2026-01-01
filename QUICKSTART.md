# Quick Start Guide

Get up and running with the replication package in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- 8GB+ RAM recommended
- ~2GB free disk space

## Step 1: Clone/Download the Repository
```bash
git clone https://github.com/mrsumitbd/LLM-generated-code-detection_Replication-Package.git
cd LLM-generated-code-detection_Replication-Package
```

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected time:** 2-5 minutes

## Step 3: Verify Installation
```bash
python verify_package.py
```

You should see:
```
✓ ALL CHECKS PASSED - Package is ready to use!
```

## Step 4: Explore the Data

### View a sample of generated code
```python
import pandas as pd

# Load Claude 3 Haiku generated functions
df = pd.read_csv('data/LLM_generated_contents_intersection/claude-3-haiku_func_level_filtered.csv')
print(f"Total samples: {len(df)}")
print(df.head())
```

### Check model performance
```python
# Load performance results
perf = pd.read_csv('results/model_performance_function_claude-3-haiku_intersection.csv')
accuracy = perf['correct'].mean()
print(f"Accuracy: {accuracy:.3f}")
```

### Load a trained model
```python
import pickle

with open('data/trained_ML_models/function_claude-3-haiku_finalized_model_intersection.pkl', 'rb') as f:
    model = pickle.load(f)
print(f"Model loaded: {type(model).__name__}")
```

## Step 5: Reproduce a Research Question

### RQ1: Feature Distribution Analysis
```bash
python src/rq1_statistical_analysis.py
```
**Output:** `results/rq1_statistical_results_detailed_intersection.csv`  
**Time:** ~5 minutes

### RQ2: Model Performance with DeLong Test
```bash
python src/rq2_delong_test.py
```
**Output:** `results/delong_test_results_intersection.csv`  
**Time:** ~2 minutes

### RQ3: Feature Importance and Overlap
```bash
python src/rq3_feature_overlap_analysis.py
```
**Output:** Multiple CSV files in `results/` and figures in `figures/`  
**Time:** ~10 minutes

### Generate SHAP Visualizations
```bash
python src/shap_analysis.py
```
**Output:** SHAP beeswarm plots and rankings in `figures/`  
**Time:** ~20-30 minutes

## Step 6: View Results

### Statistical Results (RQ1)
```python
import pandas as pd

rq1 = pd.read_csv('results/rq1_statistical_results_detailed_intersection.csv')

# Show significant features for Claude 3 Haiku (functions)
sig = rq1[
    (rq1['model'] == 'claude-3-haiku') & 
    (rq1['granularity'] == 'function') &
    (rq1['significant'] == True)
]
print(sig[['feature', 'direction', 'effect_size']])
```

### Model Comparison (RQ2)
```python
delong = pd.read_csv('results/delong_test_results_intersection.csv')

# Show significant performance differences
sig_diff = delong[delong['significant'] == True]
print(sig_diff[['model1', 'model2', 'granularity', 'auc1', 'auc2', 'p_value']])
```

### Feature Importance (RQ3)
```python
shap_vals = pd.read_csv('results/shap_values_all_configs_intersection.csv')

# Top 5 features for each configuration
top5 = shap_vals.sort_values('rank').groupby(['model', 'granularity']).head(5)
print(top5[['model', 'granularity', 'feature', 'mean_abs_shap']])
```

### View Figures
```bash
# Open a SHAP beeswarm plot
open figures/claude-3-haiku_Function_catboost_shap_beeswarm_intersection.pdf

# Open ROC curves
open figures/rq2_roc_curves.pdf

# Open feature overlap heatmap
open figures/rq3_feature_overlap_heatmaps_intersection.pdf
```

## Common Tasks

### Compare Two Models
```python
import pandas as pd

# Load performance for two models
claude = pd.read_csv('results/model_performance_function_claude-3-haiku_intersection.csv')
gpt = pd.read_csv('results/model_performance_function_gpt-3-5_intersection.csv')

print(f"Claude 3 Haiku accuracy: {claude['correct'].mean():.3f}")
print(f"GPT-3.5 accuracy: {gpt['correct'].mean():.3f}")
```

### Find Most Important Features
```python
import pandas as pd

freq = pd.read_csv('results/rq3_feature_frequency_intersection.csv')
freq_sorted = freq.sort_values('frequency', ascending=False)

print("Universal features (appear in all 8 configs):")
print(freq_sorted[freq_sorted['frequency'] == 8]['feature'].tolist())
```

### Validate on Uncontaminated Data
```bash
python src/prediction_on_uncontaminated_data.py
```

Check results:
```python
import pandas as pd
val = pd.read_csv('results/uncontaminated_validation_results.csv')
print(val[['model', 'granularity', 'accuracy', 'f1_score']])
```

## Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Memory Issues
If you encounter memory errors:
```python
# Load data in chunks
import pandas as pd
chunks = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunks:
    # Process chunk
    pass
```

### Missing Results
If result files are missing, regenerate them:
```bash
python src/rq1_statistical_analysis.py
python src/rq2_delong_test.py
python src/rq3_feature_overlap_analysis.py
```

## Next Steps

1. **Read the full paper** to understand the methodology
2. **Explore `README.md`** for detailed documentation
3. **Check `data/README.md`** for dataset details
4. **Review `src/README.md`** for script documentation
5. **Examine `results/README.md`** for result interpretations

## Getting Help

- **Documentation:** See README files in each directory
- **Verification:** Run `python verify_package.py` to check setup

## Typical Workflows

### Research Workflow (Using Existing Results)
```bash
# 1. Explore data
python  # Start Python interpreter
>>> import pandas as pd
>>> df = pd.read_csv('results/rq1_summary_counts_intersection.csv')
>>> print(df)

# 2. View visualizations
open figures/*.pdf

# 3. Done! Results already computed.
```
**Time:** 15 minutes

### Replication Workflow (Reproduce All Results)
```bash
# 1. Verify setup
python verify_package.py

# 2. Run all analyses
python src/rq1_statistical_analysis.py     # ~5 min
python src/rq2_delong_test.py              # ~2 min
python src/rq3_feature_overlap_analysis.py # ~10 min
python src/shap_analysis.py                # ~25 min

# 3. Validate results
python src/prediction_on_uncontaminated_data.py  # ~5 min

# 4. Compare with provided results
diff results/rq1_statistical_results_detailed_intersection.csv \
     results/rq1_statistical_results_detailed_intersection.csv.backup
```
**Time:** ~1 hour

## Performance Benchmarks

On a standard laptop (16GB RAM, 4-core CPU):

| Task | Time | RAM Usage |
|------|------|-----------|
| Install dependencies | 3 min | - |
| Load large CSV | 5 sec | ~2 GB |
| Train one model | 15 min | ~4 GB |
| RQ1 analysis | 5 min | ~3 GB |
| RQ2 DeLong test | 2 min | ~2 GB |
| RQ3 overlap analysis | 10 min | ~3 GB |
| SHAP analysis (1 config) | 3 min | ~4 GB |
| SHAP analysis (all 8) | 25 min | ~4 GB |

## Tips for Efficiency

1. **Use Jupyter notebooks** for interactive exploration
2. **Process configs sequentially** if memory is limited
3. **Cache intermediate results** to avoid recomputation
4. **Use `nohup`** for long-running analyses:
```bash
   nohup python src/shap_analysis.py > shap.log 2>&1 &
```

## Success Criteria

You've successfully set up the package when:
- ✓ `verify_package.py` passes all checks
- ✓ You can load a CSV file from `data/`
- ✓ You can load a trained model from `data/trained_ML_models/`
- ✓ You can run at least one RQ analysis script
- ✓ You can view at least one PDF figure

---

**Questions?** Check the main README.md or contact musfiqur.rahman@mail.concordia.ca

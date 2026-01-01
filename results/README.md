# Results Directory

This directory contains all experimental results in CSV format, organized by research question.

## File Overview

### Performance Metrics (RQ2)

#### Model Performance Files (8 files)
- `model_performance_{granularity}_{model}_intersection.csv`
- **Size:** ~46KB each
- **Rows:** Variable (depends on test set size)
- **Columns:** 
  - `sample_id`: Unique identifier
  - `true_label`: Ground truth (0=human, 1=LLM)
  - `predicted_label`: Model prediction
  - `prediction_probability`: Confidence score
  - `correct`: Boolean (prediction == true_label)

**Example usage:**
```python
import pandas as pd
perf = pd.read_csv('model_performance_function_claude-3-haiku_intersection.csv')
accuracy = perf['correct'].mean()
print(f"Accuracy: {accuracy:.3f}")
```

#### Bootstrap Confidence Intervals (8 files)
- `bootstrap_results_{granularity}_{model}_intersection.csv`
- **Size:** ~550B each
- **Columns:**
  - `metric`: Performance metric name
  - `mean`: Mean value across bootstrap samples
  - `ci_lower`: Lower bound of 95% CI
  - `ci_upper`: Upper bound of 95% CI
  - `std`: Standard deviation

**Metrics included:**
- accuracy
- precision
- recall
- f1_score
- auc_roc

**Example:**
```
metric,mean,ci_lower,ci_upper,std
accuracy,0.892,0.875,0.908,0.008
precision,0.885,0.865,0.903,0.010
recall,0.901,0.884,0.917,0.009
f1_score,0.893,0.876,0.909,0.008
auc_roc,0.945,0.932,0.957,0.006
```

#### DeLong Test Results (1 file)
- `delong_test_results_intersection.csv`
- **Size:** ~1.9KB
- **Rows:** 48 (all pairwise comparisons: 4 models × 2 granularities = 8 configs, C(8,2) = 28 pairs per granularity)
- **Columns:**
  - `model1`, `model2`: Models being compared
  - `granularity`: function or class
  - `auc1`, `auc2`: AUC-ROC for each model
  - `z_statistic`: DeLong test statistic
  - `p_value`: Statistical significance
  - `significant`: Boolean (p < 0.05 after Bonferroni correction)

**Interpretation:**
- Significant p-value → Models have statistically different performance
- Used to determine if model improvements are real or due to chance

---

### Statistical Analysis (RQ1)

#### Detailed Statistical Results (1 file)
- `rq1_statistical_results_detailed_intersection.csv`
- **Size:** ~36KB
- **Rows:** 456 (8 configs × 57 features)
- **Columns:**
  - `model`: LLM model name
  - `granularity`: function or class
  - `feature`: Feature name
  - `human_median`: Median value for human code
  - `llm_median`: Median value for LLM code
  - `u_statistic`: Mann-Whitney U statistic
  - `p_value`: Raw p-value
  - `p_value_corrected`: Holm-Bonferroni corrected p-value
  - `effect_size`: Cliff's Delta (−1 to +1)
  - `effect_magnitude`: small/medium/large/negligible
  - `significant`: Boolean (p_corrected < 0.01)
  - `direction`: upward/downward/none

**Effect Size Interpretation (Cliff's Delta):**
- |δ| < 0.147: Negligible
- 0.147 ≤ |δ| < 0.330: Small
- 0.330 ≤ |δ| < 0.474: Medium
- |δ| ≥ 0.474: Large

**Direction:**
- Upward: LLM values > Human values
- Downward: LLM values < Human values

**Example usage:**
```python
import pandas as pd
rq1 = pd.read_csv('rq1_statistical_results_detailed_intersection.csv')

# Find large effects for Claude 3 Haiku functions
large_effects = rq1[
    (rq1['model'] == 'claude-3-haiku') & 
    (rq1['granularity'] == 'function') &
    (rq1['effect_magnitude'] == 'large')
]
print(f"Found {len(large_effects)} features with large effects")
```

#### Summary Counts (1 file)
- `rq1_summary_counts_intersection.csv`
- **Size:** ~311B
- **Rows:** 8 (one per configuration)
- **Columns:**
  - `model`, `granularity`
  - `total_features`: Always 57
  - `significant_features`: Count with p < 0.01
  - `upward_divergence`: Count where LLM > Human
  - `downward_divergence`: Count where LLM < Human
  - `large_effects`: Count with |Cliff's δ| ≥ 0.474

**Key findings:**
```
model,granularity,significant_features,upward_divergence,downward_divergence,large_effects
claude-3-haiku,function,3,0,3,0
claude-3-haiku,class,23,0,23,0
gpt-3.5,function,17,0,17,5
gpt-3.5,class,29,0,29,10
gpt-oss,function,18,18,0,3
```

---

### Feature Importance (RQ3)

#### SHAP Values (1 file)
- `shap_values_all_configs_intersection.csv`
- **Size:** ~7.1KB
- **Rows:** 456 (8 configs × 57 features)
- **Columns:**
  - `model`, `granularity`, `feature`
  - `mean_abs_shap`: Mean absolute SHAP value
  - `std_shap`: Standard deviation
  - `rank`: Rank within configuration (1 = most important)
  - `scott_knott_rank`: Scott-Knott ESD group (A, B, C, D)

**Scott-Knott Groups:**
- A: Highest importance (statistically distinct)
- B: High importance
- C: Medium importance
- D: Low importance

#### Feature Rankings (1 file)
- `feature_rankings_all_configs_intersection.csv`
- **Size:** ~7.4KB
- **Rows:** 456
- **Columns:**
  - `model`, `granularity`, `feature`
  - `shap_rank`: Rank by SHAP importance
  - `scott_knott_rank`: Statistical grouping
  - `in_top10`: Boolean

#### Feature Importance Summary (1 file)
- `feature_importance_summary_intersection.csv`
- **Size:** ~2.9KB
- **Rows:** 57 (one per feature)
- **Columns:**
  - `feature`
  - `appears_in_top10_count`: How many configs include this in top-10
  - `mean_rank_across_configs`: Average rank (1-57)
  - `min_rank`, `max_rank`: Best and worst ranks

**Most important features (appear in top-10 most often):**
1. cyclomatic_complexity (8/8 configs)
2. max_nesting_depth (8/8 configs)
3. avg_line_length (7/8 configs)
4. num_parameters (7/8 configs)
5. ratio_comment_to_code (6/8 configs)

#### Model Importance Statistics (1 file)
- `model_importance_statistics_intersection.csv`
- **Size:** ~559B
- **Rows:** 8
- **Columns:**
  - `model`, `granularity`
  - `num_features_in_top10`: Always 10
  - `mean_shap_top10`: Average importance of top-10 features
  - `concentration_ratio`: Sum(top-10) / Sum(all 57)

**Interpretation:**
- Higher concentration → Top features dominate predictions
- Lower concentration → More distributed importance

#### Statistical Tests Summary (1 file)
- `statistical_tests_intersection.csv`
- **Size:** ~301B
- **Rows:** 8
- **Columns:**
  - `model`, `granularity`
  - `permutation_test_p_value`: Significance of feature importance
  - `kruskal_wallis_p_value`: Test for differences across features

---

### Feature Overlap Analysis (RQ3)

#### Jaccard Similarity Matrices (2 files)

**Function-level:**
- `rq3_function_jaccard_matrix_intersection.csv`
- **Size:** ~251B
- **Format:** 4×4 matrix (models as rows and columns)
- **Values:** Jaccard similarity coefficients (0-1)

**Class-level:**
- `rq3_class_jaccard_matrix_intersection.csv`
- **Size:** ~283B
- **Format:** 4×4 matrix

**Jaccard Similarity Formula:**
J(A,B) = |A ∩ B| / |A ∪ B|

Where A and B are sets of top-10 features for two models.

**Example:**
```
,claude-3-haiku,claude-4-5-haiku,gpt-3.5,gpt-oss
claude-3-haiku,1.000,0.636,0.545,0.500
claude-4-5-haiku,0.636,1.000,0.583,0.538
gpt-3.5,0.545,0.583,1.000,0.615
gpt-oss,0.500,0.538,0.615,1.000
```

**Interpretation:**
- 1.0 = Perfect overlap (diagonal)
- 0.5-0.7 = Moderate overlap
- <0.5 = Low overlap

#### Feature Frequency (1 file)
- `rq3_feature_frequency_intersection.csv`
- **Size:** ~816B
- **Rows:** Variable (unique features appearing in any top-10)
- **Columns:**
  - `feature`: Feature name
  - `frequency`: Count of configs where feature is in top-10 (0-8)
  - `percentage`: frequency / 8 * 100

**Top universal features (frequency = 8):**
- cyclomatic_complexity
- max_nesting_depth
- num_lines

#### Granularity Overlap (1 file)
- `rq3_granularity_overlap_intersection.csv`
- **Size:** ~261B
- **Rows:** 4 (one per model)
- **Columns:**
  - `model`
  - `function_top10`: Set of top-10 features for functions
  - `class_top10`: Set of top-10 features for classes
  - `overlap_count`: |function_top10 ∩ class_top10|
  - `jaccard_similarity`: J(function_top10, class_top10)

**Example:**
```
model,overlap_count,jaccard_similarity
claude-3-haiku,6,0.462
gpt-3.5,7,0.538
```

**Interpretation:**
- Higher overlap → Same features important across granularities
- Lower overlap → Granularity affects feature importance

#### Summary Statistics (1 file)
- `rq3_summary_statistics_intersection.csv`
- **Size:** ~287B
- **Rows:** 2 (function and class)
- **Columns:**
  - `granularity`
  - `mean_top10_overlap`: Average pairwise Jaccard across models
  - `median_top10_overlap`
  - `total_unique_features`: Count of distinct features in any top-10
  - `universal_features`: Count appearing in all 4 models

---

### Validation Results

#### Uncontaminated Validation (1 file)
- `uncontaminated_validation_results.csv`
- **Size:** ~1.0KB
- **Rows:** 8
- **Columns:**
  - `model`, `granularity`
  - `test_samples`: Number of uncontaminated samples
  - `accuracy`, `precision`, `recall`, `f1_score`, `auc_roc`
  - `performance_drop`: Difference from main test set

**Purpose:**
- Verify models generalize to post-2024 data
- Detect potential training data contamination
- Expected: Small performance drop (<5%)

**Example:**
```
model,granularity,test_samples,accuracy,f1_score,performance_drop
claude-3-haiku,function,750,0.876,0.881,0.016
```

---

### Additional Metrics

#### Selected Features (8 files)
- `selected_features_{granularity}_{model}_intersection.csv`
- **Size:** 90-233B each
- **Columns:**
  - `feature`: Feature name
  - `selection_method`: How it was selected (e.g., mutual_info, shap)
  - `score`: Selection score

**Note:** Some configs have very few features (e.g., 90B = only 1-2 features selected by automatic feature selection during training).

#### Comment-to-Code Ratio Analysis (1 file)
- `ratiocommenttocode_analysis_intersection.csv`
- **Size:** ~508B
- **Rows:** 8
- **Columns:**
  - `model`, `granularity`
  - `human_mean`, `human_std`
  - `llm_mean`, `llm_std`
  - `difference`: llm_mean - human_mean
  - `p_value`: Mann-Whitney U test

**Insight:**
- LLM code often has different commenting patterns
- Can be discriminative feature

---

## Data Formats

### CSV Standards
- **Delimiter:** Comma (`,`)
- **Encoding:** UTF-8
- **Missing values:** Empty string or `NaN`
- **Decimal separator:** Period (`.`)
- **Float precision:** 3-6 decimal places

### Naming Conventions
- `{granularity}`: `function` or `class`
- `{model}`: `claude-3-haiku`, `claude-4-5-haiku`, `gpt-3.5`, `gpt-oss`
- `_intersection`: Indicates global intersection dataset

---

## Usage Examples

### Loading All Performance Metrics
```python
import pandas as pd
import glob

# Load all model performance files
perf_files = glob.glob('model_performance_*_intersection.csv')
all_results = []

for file in perf_files:
    df = pd.read_csv(file)
    # Extract model and granularity from filename
    parts = file.replace('model_performance_', '').replace('_intersection.csv', '').split('_')
    df['model'] = '_'.join(parts[1:])
    df['granularity'] = parts[0]
    all_results.append(df)

combined = pd.concat(all_results, ignore_index=True)
print(combined.groupby(['model', 'granularity'])['correct'].mean())
```

### Analyzing Feature Importance
```python
import pandas as pd

# Load SHAP values
shap = pd.read_csv('shap_values_all_configs_intersection.csv')

# Top 5 features per configuration
top5 = shap.sort_values('rank').groupby(['model', 'granularity']).head(5)
print(top5[['model', 'granularity', 'feature', 'mean_abs_shap']])

# Universal features (important across all configs)
feature_freq = pd.read_csv('rq3_feature_frequency_intersection.csv')
universal = feature_freq[feature_freq['frequency'] == 8]
print(f"Universal features: {list(universal['feature'])}")
```

### Comparing Models Statistically
```python
import pandas as pd

# Load DeLong test results
delong = pd.read_csv('delong_test_results_intersection.csv')

# Filter for significant differences
sig_diff = delong[delong['significant'] == True]
print(f"Found {len(sig_diff)} significant performance differences")

# Show pairwise comparisons
for _, row in sig_diff.iterrows():
    print(f"{row['model1']} vs {row['model2']} ({row['granularity']}): "
          f"AUC={row['auc1']:.3f} vs {row['auc2']:.3f}, p={row['p_value']:.4f}")
```

---

## Reproducing Results

All CSV files in this directory can be regenerated by running the corresponding analysis scripts:
```bash
# RQ1 results
python ../src/rq1_statistical_analysis.py
# → Generates rq1_*.csv

# RQ2 results
python ../src/model_training.py  # For all 8 configs
python ../src/rq2_delong_test.py
# → Generates model_performance_*.csv, bootstrap_results_*.csv, delong_test_*.csv

# RQ3 results
python ../src/shap_analysis.py
python ../src/rq3_feature_overlap_analysis.py
# → Generates shap_*.csv, rq3_*.csv, feature_*.csv

# Validation
python ../src/prediction_on_uncontaminated_data.py
# → Generates uncontaminated_validation_results.csv
```

---

## File Integrity

To verify data integrity, check file sizes and row counts:
```bash
# Count rows in all CSV files
for file in *.csv; do
    echo "$file: $(tail -n +2 $file | wc -l) rows"
done

# Expected totals:
# - 8 model_performance files: ~1000-2000 rows each
# - 8 bootstrap_results files: 5 rows each
# - 1 delong_test: 48 rows
# - 1 rq1_detailed: 456 rows
# - 1 shap_values: 456 rows
```
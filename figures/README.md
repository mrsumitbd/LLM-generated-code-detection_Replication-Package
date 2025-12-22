# Figures Directory

This directory contains all publication-quality figures in PDF format.

## Overview

All figures are vector-based PDFs suitable for publication. Figures are organized by research question and type.

## File Organization

### RQ2: Model Performance (2 files)

#### `rq2_confusion_matrices.pdf`
- **Size:** ~28KB
- **Dimensions:** Multi-panel figure (2×4 grid)
- **Content:** Confusion matrices for all 8 configurations
  - Rows: 2 granularities (function, class)
  - Columns: 4 models (Claude 3 Haiku, Claude 4.5 Haiku, GPT-3.5, GPT-OSS)
- **Format:** Heatmap with counts
- **Color scheme:** Blue gradient
- **Annotations:** 
  - True Positive (TP), False Positive (FP)
  - False Negative (FN), True Negative (TN)
  - Accuracy percentages

**Usage in paper:** Figure showing classification performance across models

#### `rq2_roc_curves.pdf`
- **Size:** ~97KB
- **Dimensions:** Multi-panel figure (2×1 layout)
- **Content:** ROC curves comparing all 4 models
  - Top panel: Function-level
  - Bottom panel: Class-level
- **Format:** Line plot with AUC annotations
- **Color scheme:** Distinct colors per model
- **Elements:**
  - Diagonal reference line (random classifier)
  - AUC-ROC values in legend
  - 95% confidence intervals (shaded regions)

**Usage in paper:** Figure demonstrating discriminative power

---

### RQ3: Feature Importance - SHAP Analysis (8 files)

#### SHAP Beeswarm Plots (8 PDFs)
Pattern: `{model}_{granularity}_catboost_shap_beeswarm_intersection.pdf`

**Files:**
1. `claude-3-haiku_Function_catboost_shap_beeswarm_intersection.pdf` (93KB)
2. `claude-3-haiku_Class_catboost_shap_beeswarm_intersection.pdf` (134KB)
3. `claude-4-5-haiku_Function_catboost_shap_beeswarm_intersection.pdf` (98KB)
4. `claude-4-5-haiku_Class_catboost_shap_beeswarm_intersection.pdf` (98KB)
5. `gpt-3-5_Function_catboost_shap_beeswarm_intersection.pdf` (95KB)
6. `gpt-3-5_Class_catboost_shap_beeswarm_intersection.pdf` (133KB)
7. `gpt-oss_Function_catboost_shap_beeswarm_intersection.pdf` (135KB)
8. `gpt-oss_Class_catboost_shap_beeswarm_intersection.pdf` (113KB)

**Content:** Top-10 most important features ranked by mean absolute SHAP value

**Visual elements:**
- **Y-axis:** Features (ordered by importance, top = most important)
- **X-axis:** SHAP value (impact on prediction)
  - Positive → Increases probability of "LLM-generated" classification
  - Negative → Increases probability of "human-written" classification
- **Color:** Feature value (red = high, blue = low)
- **Density:** Horizontal spread shows distribution across samples

**Interpretation guide:**
- Wide spread → Feature has variable impact
- Consistent direction → Feature reliably predicts class
- Color separation → High vs. low values have opposite effects

**Example interpretation:**
If `cyclomatic_complexity` shows:
- Red dots (high values) on positive side → High complexity suggests LLM code
- Blue dots (low values) on negative side → Low complexity suggests human code

---

### RQ3: Feature Rankings - Scott-Knott ESD (8 files)

#### Ranking Plots (8 PDFs)
Pattern: `{Granularity}_{model}_ranking.pdf`

**Files:**
1. `Function_claude-3-haiku_ranking.pdf` (6.1KB)
2. `Function_claude-4-5-haiku_ranking.pdf` (7.5KB)
3. `Function_gpt-3-5_ranking.pdf` (6.0KB)
4. `Function_gpt-oss_ranking.pdf` (9.2KB)
5. `Class_claude-3-haiku_ranking.pdf` (5.8KB)
6. `Class_claude-4-5-haiku_ranking.pdf` (5.9KB)
7. `Class_gpt-3-5_ranking.pdf` (6.5KB)
8. `Class_gpt-oss_ranking.pdf` (6.2KB)

**Content:** Feature importance grouped by statistical significance (Scott-Knott ESD test)

**Visual elements:**
- **Y-axis:** Mean absolute SHAP value
- **X-axis:** Features (grouped by Scott-Knott rank)
- **Groups:** Labeled A, B, C, D (A = highest importance)
- **Colors:** Different color per statistical group
- **Error bars:** Standard deviation of SHAP values

**Scott-Knott ESD Groups:**
- **Group A:** Statistically most important features
- **Group B:** High importance (significantly lower than A)
- **Group C:** Medium importance
- **Group D:** Low importance (not significantly different from random)

**Usage in paper:** Combined 8-panel figure showing feature rankings across all configurations

---

### RQ3: Feature Overlap Analysis (4 files)

#### `rq3_feature_overlap_heatmaps_intersection.pdf`
- **Size:** ~28KB
- **Dimensions:** 2×1 panel layout
- **Content:** Jaccard similarity matrices
  - Top: Function-level overlap between models
  - Bottom: Class-level overlap between models
- **Format:** 4×4 heatmap (one per model pair)
- **Color scheme:** Blue gradient (darker = higher similarity)
- **Annotations:** Jaccard coefficient values (0-1)

**Interpretation:**
- Diagonal = 1.0 (model compared to itself)
- Off-diagonal values show feature set overlap
- Higher values → Models rely on similar features

#### `rq3_feature_frequency_intersection.pdf`
- **Size:** ~33KB
- **Dimensions:** Single panel
- **Content:** Bar chart showing how often each feature appears in top-10
- **X-axis:** Feature names
- **Y-axis:** Frequency (0-8 configurations)
- **Colors:** Gradient based on frequency
- **Highlighted:** Universal features (frequency = 8)

**Key insight:** Identifies features important across all models and granularities

#### `feature_importance_heatmap_intersection.pdf`
- **Size:** ~36KB
- **Dimensions:** Single panel
- **Content:** Heatmap of mean absolute SHAP across all 57 features × 8 configs
- **Rows:** Features (57)
- **Columns:** Configurations (4 models × 2 granularities)
- **Color scheme:** Red-white-blue diverging
  - Red = High importance
  - White = Medium importance
  - Blue = Low importance
- **Ordering:** Features sorted by overall importance

**Usage:** Overview of feature importance patterns

#### `feature_importance_heatmap_top10_intersection.pdf`
- **Size:** ~31KB
- **Dimensions:** Single panel
- **Content:** Same as above, but only top-10 features per configuration
- **Rows:** Unique features that appear in any top-10 (~20-25 features)
- **Focused view:** Easier to see patterns in most important features

---

## Figure Specifications

### Technical Details

**Format:** PDF (Portable Document Format)
- Vector graphics (scalable without quality loss)
- Embedded fonts
- CMYK color space (print-ready)

**Resolution:** 
- Vector elements: Infinite resolution
- Raster elements (if any): 300 DPI minimum

**Fonts:**
- Primary: Arial or Helvetica
- Math/equations: Computer Modern or Times New Roman
- Size: 10-12pt for body text, 8pt minimum for annotations

**Color Palettes:**
- **Sequential:** Blues (low to high intensity)
- **Diverging:** Blue-White-Red (negative to positive)
- **Categorical:** Colorblind-friendly palette (Wong 2011)
- **SHAP:** Red (high feature value) to Blue (low feature value)

**Dimensions:**
- Single-column figures: 3.5" width
- Double-column figures: 7" width
- Height: Variable (typically 3-5")
- Multi-panel: Maintain consistent aspect ratios

---

## Generating Figures

All figures can be regenerated using the source scripts:

### SHAP Beeswarm Plots
```bash
python ../src/shap_analysis.py
# Generates all 8 *_shap_beeswarm_intersection.pdf files
```

### Scott-Knott Rankings
```bash
python ../src/shap_analysis.py
# Also generates all 8 *_ranking.pdf files
# Uses R script: ../src/scott-knott-esd.R
```

### RQ2 Performance Figures
```bash
# Confusion matrices and ROC curves
# Generated during model training/evaluation
python ../src/model_training.py  # Creates confusion matrices
# ROC curves generated from model_performance_*.csv files
```

### RQ3 Overlap Analysis
```bash
python ../src/rq3_feature_overlap_analysis.py
# Generates:
# - rq3_feature_overlap_heatmaps_intersection.pdf
# - rq3_feature_frequency_intersection.pdf
# - feature_importance_heatmap_intersection.pdf
# - feature_importance_heatmap_top10_intersection.pdf
```

---

## Usage in Paper

### Recommended Figure Placement

**RQ1 (Feature Distributions):**
- No figures in this directory
- Results presented in tables (see `../results/rq1_*.csv`)

**RQ2 (Detection Performance):**
- **Figure 1:** `rq2_roc_curves.pdf` - ROC curves showing model performance
- **Figure 2:** `rq2_confusion_matrices.pdf` - Detailed classification results

**RQ3 (Feature Importance):**
- **Figure 3:** Combined 8-panel SHAP beeswarm (all 8 `*_shap_beeswarm_intersection.pdf`)
- **Figure 4:** Combined 8-panel rankings (all 8 `*_ranking.pdf`)
- **Figure 5:** `rq3_feature_overlap_heatmaps_intersection.pdf` - Model comparison
- **Figure 6:** `rq3_feature_frequency_intersection.pdf` - Universal features

**Supplementary Material:**
- `feature_importance_heatmap_intersection.pdf` - Full heatmap
- `feature_importance_heatmap_top10_intersection.pdf` - Focused heatmap

### LaTeX Integration
```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/rq2_roc_curves.pdf}
  \caption{ROC curves comparing detection performance across four LLMs at function-level (top) and class-level (bottom) granularities. All models achieve AUC-ROC > 0.85, with Claude 4.5 Haiku showing the highest performance.}
  \label{fig:roc_curves}
\end{figure}
```

---

## Customization

### Modifying Figures

To customize figure appearance, edit the plotting functions in:
- `../src/shap_analysis.py` - SHAP plots and rankings
- `../src/rq3_feature_overlap_analysis.py` - Overlap heatmaps
- `../src/model_training.py` - Confusion matrices

**Common modifications:**
```python
# Change color scheme
plt.style.use('seaborn-colorblind')

# Adjust figure size
fig, ax = plt.subplots(figsize=(10, 6))

# Change font size
plt.rcParams.update({'font.size': 12})

# Save with higher DPI (for presentations)
plt.savefig('output.pdf', dpi=600, bbox_inches='tight')
```

### Creating Combined Figures

For multi-panel figures in the paper:
```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Create 2x4 grid for all SHAP plots
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

models = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3.5', 'gpt-oss']
granularities = ['Function', 'Class']

for i, gran in enumerate(granularities):
    for j, model in enumerate(models):
        ax = axes[i, j]
        # Plot SHAP beeswarm on this axis
        # ... plotting code ...
        ax.set_title(f"{model} ({gran})")

plt.tight_layout()
plt.savefig('combined_shap_beeswarm.pdf', bbox_inches='tight')
```

---

## Quality Checklist

Before using figures in publication:

- [ ] All text is readable at final size
- [ ] Axis labels are clear and informative
- [ ] Legends are present and unambiguous
- [ ] Colors are distinguishable (colorblind-safe)
- [ ] No overlapping text or elements
- [ ] Consistent font sizes across figures
- [ ] High-quality vector graphics (no pixelation)
- [ ] Proper citation of tools used (SHAP, scikit-learn, etc.)

---

## File Size Summary

| Figure Type | Count | Size Range | Total Size |
|-------------|-------|------------|------------|
| SHAP Beeswarm | 8 | 93-135 KB | ~900 KB |
| Rankings | 8 | 5.8-9.2 KB | ~52 KB |
| RQ2 Performance | 2 | 28-97 KB | ~125 KB |
| RQ3 Overlap | 4 | 28-36 KB | ~128 KB |
| **Total** | **22** | - | **~1.2 MB** |

---

## Accessibility

All figures follow accessibility best practices:
- Colorblind-friendly palettes
- High contrast ratios
- Text alternatives provided in captions
- Multiple encoding channels (color + shape + position)

---

## Contact

For questions about figure generation or customization: [Your email]

## Software Used

- **Python 3.8+** with matplotlib, seaborn
- **SHAP library** for beeswarm plots
- **R** for Scott-Knott ESD ranking
- **scikit-learn** for confusion matrices and ROC curves

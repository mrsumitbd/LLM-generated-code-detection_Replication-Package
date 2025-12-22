# Replication Package Contents

This document provides a comprehensive inventory of all files in the replication package.

**Last Updated:** 2025-01-22  
**Version:** 1.0.0  
**Total Size:** ~800 MB (compressed: ~200 MB)

## Directory Tree
```
LLM-generated-code-detection_Replication-Package/
├── README.md                           # Main documentation
├── LICENSE                             # MIT License
├── CITATION.cff                        # Citation metadata
├── requirements.txt                    # Python dependencies
├── verify_package.py                   # Verification script
├── PACKAGE_CONTENTS.md                 # This file
│
├── data/                               # ~780 MB
│   ├── README.md
│   ├── LLM_generated_contents_intersection/    # 10 CSV files, ~780 MB
│   ├── features_for_ML/                        # 7,083 CSV files, ~50 MB
│   │   ├── class_global_intersection/
│   │   ├── function_global_intersection/
│   │   └── uncontaminated/
│   ├── trained_ML_models/                      # 8 .pkl files, ~9 MB
│   ├── data_for_ML_validation/                 # 8 CSV files, ~1.5 MB
│   ├── uncontaminated_intersection_keys_class.txt     # 46 KB
│   └── uncontaminated_intersection_keys_function.txt  # 69 KB
│
├── src/                                # ~200 KB
│   ├── README.md
│   ├── batch_generate_with_anthropicai.py      # Code generation
│   ├── batch_generation_with_openai.py
│   ├── generation_with_togetherai.py
│   ├── prepare_for_understand.py               # Feature extraction prep
│   ├── model_training.py                       # CatBoost training
│   ├── rq1_statistical_analysis.py             # RQ1 analysis
│   ├── rq2_delong_test.py                      # RQ2 DeLong test
│   ├── rq3_feature_overlap_analysis.py         # RQ3 overlap analysis
│   ├── shap_analysis.py                        # SHAP computation
│   ├── prediction_on_uncontaminated_data.py    # Validation
│   ├── uncontaminated_intersection_analysis.py
│   └── utility.py                              # Helper functions
│
├── results/                            # ~600 KB
│   ├── README.md
│   ├── model_performance_*.csv                 # 8 files, ~368 KB
│   ├── bootstrap_results_*.csv                 # 8 files, ~4.4 KB
│   ├── selected_features_*.csv                 # 8 files, ~1.5 KB
│   ├── rq1_statistical_results_detailed_intersection.csv   # 36 KB
│   ├── rq1_summary_counts_intersection.csv     # 311 B
│   ├── delong_test_results_intersection.csv    # 1.9 KB
│   ├── shap_values_all_configs_intersection.csv            # 7.1 KB
│   ├── feature_importance_summary_intersection.csv         # 2.9 KB
│   ├── feature_rankings_all_configs_intersection.csv       # 7.4 KB
│   ├── model_importance_statistics_intersection.csv        # 559 B
│   ├── statistical_tests_intersection.csv      # 301 B
│   ├── ratiocommenttocode_analysis_intersection.csv        # 508 B
│   ├── rq3_*_intersection.csv                  # 5 files, ~2 KB
│   └── uncontaminated_validation_results.csv   # 1.0 KB
│
└── figures/                            # ~1.2 MB
    ├── README.md
    ├── *_shap_beeswarm_intersection.pdf        # 8 files, ~900 KB
    ├── *_ranking.pdf                           # 8 files, ~52 KB
    ├── rq2_confusion_matrices.pdf              # 28 KB
    ├── rq2_roc_curves.pdf                      # 97 KB
    ├── rq3_feature_frequency_intersection.pdf  # 33 KB
    ├── rq3_feature_overlap_heatmaps_intersection.pdf       # 28 KB
    ├── feature_importance_heatmap_intersection.pdf         # 36 KB
    └── feature_importance_heatmap_top10_intersection.pdf   # 31 KB
```

## File Counts by Type

| Type | Count | Total Size |
|------|-------|------------|
| Python scripts (.py) | 12 | ~200 KB |
| CSV data files | 7,120 | ~832 MB |
| Trained models (.pkl) | 8 | ~9 MB |
| Result files (.csv) | 38 | ~600 KB |
| Figure files (.pdf) | 22 | ~1.2 MB |
| Documentation (.md) | 6 | ~120 KB |
| Other | 4 | ~5 KB |
| **TOTAL** | **7,210** | **~843 MB** |

## Key Statistics

### Data
- **Generated Code Samples:** 
  - Function-level: ~60,000 samples (4 models × ~15,000 each)
  - Class-level: ~40,000 samples (4 models × ~10,000 each)
- **Intersection Size:** ~15,000 functions, ~10,000 classes
- **Features Extracted:** 57 metrics per sample
- **Trained Models:** 8 configurations (4 models × 2 granularities)

### Experiments
- **Statistical Tests:** 456 Mann-Whitney U tests (RQ1)
- **Model Evaluations:** 8 classifiers with 5-fold CV
- **DeLong Tests:** 28 pairwise comparisons per granularity
- **SHAP Computations:** 8 configurations × test set size
- **Uncontaminated Validation:** 1,000 classes + 1,500 functions

### Outputs
- **Performance Metrics:** 8 detailed CSV files
- **Statistical Results:** 38 CSV files
- **Visualizations:** 22 publication-quality PDFs

## Reproducibility

### Without Regenerating Data
**Time Required:** ~1-2 hours  
**Commands:**
```bash
pip install -r requirements.txt
python src/rq1_statistical_analysis.py
python src/rq2_delong_test.py
python src/rq3_feature_overlap_analysis.py
python src/shap_analysis.py
python src/prediction_on_uncontaminated_data.py
```

### Full Pipeline (Optional)
**Time Required:** ~8-12 hours  
**Requirements:** 
- API keys (Anthropic, OpenAI, Together AI)
- SciTools Understand™ license
- 16GB+ RAM

**Not recommended** - use provided data instead.

## Data Provenance

### Sources
1. **CodeSearchNet Dataset (Python subset)**
   - Original repository: https://github.com/github/CodeSearchNet
   - Functions: ~400,000 samples
   - Classes: ~100,000 samples
   - License: Original CodeSearchNet license

2. **LLM-Generated Code**
   - Generated using: Claude 3 Haiku, Claude 4.5 Haiku, GPT-3.5, GPT-OSS
   - Temperature: 0.7
   - Prompt: "Generate Python code for: {docstring}"
   - Generation period: 2024-11-18 to 2024-12-01

3. **Post-2024 Validation Data**
   - Extracted from repositories created after 2024-01-01
   - Ensures contamination-free validation
   - Sources: GitHub public repositories

### Processing
1. **Intersection Selection:** Global intersection across all 4 models
2. **Feature Extraction:** SciTools Understand™ (57 metrics)
3. **Train/Test Split:** 80/20 stratified split
4. **Model Training:** CatBoost with grid search CV

## Checksums (for verification)
```
# MD5 checksums for key files
data/trained_ML_models/function_claude-3-haiku_finalized_model_intersection.pkl: [generate actual checksum]
results/rq1_statistical_results_detailed_intersection.csv: [generate actual checksum]
results/shap_values_all_configs_intersection.csv: [generate actual checksum]
```

## Version History

### v1.0.0 (2025-01-22)
- Initial release for TOSEM/EMSE submission
- Complete replication package
- All 8 model configurations
- Global intersection methodology
- Contamination-free validation

## Usage Notes

1. **Data Files:** All CSV files use UTF-8 encoding with comma delimiters
2. **Models:** Trained models are Python pickle files (requires Python 3.8+)
3. **Scripts:** All scripts have inline documentation and argument parsing
4. **Figures:** Vector PDFs suitable for publication (300+ DPI equivalent)

## System Requirements

### Minimum
- **OS:** Linux, macOS, or Windows
- **Python:** 3.8 or higher
- **RAM:** 8 GB
- **Storage:** 2 GB free space

### Recommended
- **OS:** Linux or macOS
- **Python:** 3.10
- **RAM:** 16 GB
- **Storage:** 5 GB free space
- **CPU:** 4+ cores for parallel processing

## Known Limitations

1. **Feature Extraction:** Requires SciTools Understand™ (commercial) to regenerate features
2. **API Costs:** Regenerating code requires paid API access to LLM providers
3. **Computation Time:** SHAP analysis can take 15-30 minutes per configuration
4. **Memory Usage:** Loading all features simultaneously requires ~8GB RAM

## Contact Information

**Primary Contact:** [Your Name] ([Your Email])  
**Institution:** Concordia University  
**Advisor:** Dr. Emad Shihab  
**Repository:** [GitHub URL]  
**Issues:** [GitHub Issues URL]

## Citation

Please cite our paper when using this package:
```bibtex
@article{yourpaper2025,
  title={Your Paper Title},
  author={Your Name and Emad Shihab},
  journal={TOSEM/EMSE},
  year={2025}
}
```

## Acknowledgments

- CodeSearchNet dataset creators
- SciTools, Inc. for Understand™
- Anthropic, OpenAI, and Together AI for API access
- Concordia University for compute resources

---

**Package prepared by:** [Your Name]  
**Date:** 2025-01-22  
**For questions:** [Your Email]

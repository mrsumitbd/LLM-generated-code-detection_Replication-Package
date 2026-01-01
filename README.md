# Replication Package: Detecting LLM-Generated Code

This repository contains the complete replication package for our paper on detecting LLM-generated code across multiple models and granularities.

## Paper Information

**Title:** Automatic Detection of LLM-Generated Code: A Comparative Case Study of Contemporary Models Across Function and Class Granularities

**Authors:** Musfiqur Rahman, SayedHassan Khatoonabadi, Ahmad Abdellatif, Emad Shihab  

**Venue:** Submitted to EMSE

**Year:** 2025

## Overview

This replication package enables full reproduction of our experimental results, including:
- Statistical analysis of feature distributions (RQ1)
- Model performance evaluation with DeLong tests (RQ2)  
- Feature importance and overlap analysis (RQ3)
- Validation on contamination-free datasets

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


## Research Questions

### RQ1: Feature Distribution Analysis
**Question:** How do feature distributions differ between human-written and LLM-generated code?

**Script:** `src/rq1_statistical_analysis.py`  
**Results:** `results/rq1_statistical_results_detailed_intersection.csv`  

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
@article{rahman2025automaticdetectionllmgeneratedcode,
      title={Automatic Detection of LLM-Generated Code: A Comparative Case Study of Contemporary Models Across Function and Class Granularities}, 
      author={Musfiqur Rahman and SayedHassan Khatoonabadi and Ahmad Abdellatif and Emad Shihab},
      year={2025},
      eprint={2409.01382},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2409.01382}, 
}
```

## License

MIT

The original CodeSearchNet dataset is licensed under MIT.

## Contact

For questions or issues:
- **Primary Contact:** musfiqur.rahman@mail.concordia.ca

## Acknowledgments

- CodeSearchNet dataset: GitHub and collaborators
- SciTools Understand™: SciTools, Inc.

## Changelog

### v1.0.0 (2025-01-28)
- Initial release for EMSE submission
- Complete replication package with all data, code, and results

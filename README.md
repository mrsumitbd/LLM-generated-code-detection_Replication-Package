# Replication Package: Detecting LLM-Generated Code

This repository contains the complete replication package for our paper on detecting LLM-generated code across multiple models and granularities.

## Paper Information

**Title:** Automatic Detection of LLM-Generated Code: A Comparative Case Study of Contemporary Models Across Function and Class Granularities
**Authors:** Musfiqur Rahman, SayedHassan Khatoonabadi, Ahmad Abdellatif, Emad Shihab  
**Venue:** [Submitted to EMSE]  
**Year:** 2025

## Overview

This replication package enables full reproduction of our experimental results, including:
- Statistical analysis of feature distributions (RQ1)
- Model performance evaluation with DeLong tests (RQ2)  
- Feature importance and overlap analysis (RQ3)
- Validation on contamination-free datasets


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

[Specify license - e.g., MIT, Apache 2.0]

The original CodeSearchNet dataset is licensed under [original license].

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

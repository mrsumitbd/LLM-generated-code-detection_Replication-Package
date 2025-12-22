#!/usr/bin/env python3
"""
Verification script for the replication package.
Checks that all required files and dependencies are present.
"""

import os
import sys
import importlib
from pathlib import Path

def check_dependencies():
    """Check if all required Python packages are installed."""
    required_packages = [
        'pandas', 'numpy', 'scipy', 'sklearn', 'catboost', 
        'shap', 'matplotlib', 'seaborn', 'statsmodels'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            else:
                importlib.import_module(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} NOT installed")
    
    return missing

def check_data_files():
    """Check if required data files exist."""
    data_checks = {
        'Generated Code': 'data/LLM_generated_contents_intersection',
        'Features': 'data/features_for_ML',
        'Trained Models': 'data/trained_ML_models',
        'Test Data': 'data/data_for_ML_validation',
    }
    
    missing = []
    for name, path in data_checks.items():
        if os.path.exists(path):
            num_files = len(list(Path(path).rglob('*')))
            print(f"✓ {name}: {path} ({num_files} files)")
        else:
            missing.append(name)
            print(f"✗ {name}: {path} NOT FOUND")
    
    return missing

def check_scripts():
    """Check if all analysis scripts exist."""
    required_scripts = [
        'src/model_training.py',
        'src/rq1_statistical_analysis.py',
        'src/rq2_delong_test.py',
        'src/rq3_feature_overlap_analysis.py',
        'src/shap_analysis.py',
        'src/utility.py'
    ]
    
    missing = []
    for script in required_scripts:
        if os.path.exists(script):
            print(f"✓ {script}")
        else:
            missing.append(script)
            print(f"✗ {script} NOT FOUND")
    
    return missing

def check_results():
    """Check if result files exist."""
    result_files = [
        'results/rq1_statistical_results_detailed_intersection.csv',
        'results/delong_test_results_intersection.csv',
        'results/shap_values_all_configs_intersection.csv',
    ]
    
    missing = []
    for file in result_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"✓ {file} ({size:.1f} KB)")
        else:
            missing.append(file)
            print(f"✗ {file} NOT FOUND")
    
    return missing

def check_figures():
    """Check if figure files exist."""
    if os.path.exists('figures'):
        pdf_files = list(Path('figures').glob('*.pdf'))
        print(f"✓ Figures directory: {len(pdf_files)} PDF files")
        return []
    else:
        print(f"✗ Figures directory NOT FOUND")
        return ['figures/']

def test_data_loading():
    """Test loading a sample dataset."""
    try:
        import pandas as pd
        
        # Try loading a result file
        test_file = 'results/rq1_summary_counts_intersection.csv'
        if os.path.exists(test_file):
            df = pd.read_csv(test_file)
            print(f"✓ Successfully loaded {test_file}")
            print(f"  Shape: {df.shape}")
            return True
        else:
            print(f"✗ Test file not found: {test_file}")
            return False
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def test_model_loading():
    """Test loading a trained model."""
    try:
        import pickle
        
        model_file = 'data/trained_ML_models/function_claude-3-haiku_finalized_model_intersection.pkl'
        if os.path.exists(model_file):
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
            print(f"✓ Successfully loaded trained model")
            print(f"  Model type: {type(model).__name__}")
            return True
        else:
            print(f"✗ Test model not found: {model_file}")
            return False
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

def main():
    print("=" * 70)
    print("REPLICATION PACKAGE VERIFICATION")
    print("=" * 70)
    
    all_good = True
    
    print("\n1. Checking Python Dependencies...")
    print("-" * 70)
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"\n⚠ Missing packages: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt")
        all_good = False
    
    print("\n2. Checking Data Files...")
    print("-" * 70)
    missing_data = check_data_files()
    if missing_data:
        print(f"\n⚠ Missing data: {', '.join(missing_data)}")
        all_good = False
    
    print("\n3. Checking Analysis Scripts...")
    print("-" * 70)
    missing_scripts = check_scripts()
    if missing_scripts:
        print(f"\n⚠ Missing scripts: {', '.join(missing_scripts)}")
        all_good = False
    
    print("\n4. Checking Results...")
    print("-" * 70)
    missing_results = check_results()
    if missing_results:
        print(f"\n⚠ Missing results: {', '.join(missing_results)}")
        print("Run analysis scripts to regenerate results")
    
    print("\n5. Checking Figures...")
    print("-" * 70)
    missing_figs = check_figures()
    if missing_figs:
        print(f"\n⚠ Missing figures")
        print("Run visualization scripts to regenerate figures")
    
    print("\n6. Testing Data Loading...")
    print("-" * 70)
    if not test_data_loading():
        all_good = False
    
    print("\n7. Testing Model Loading...")
    print("-" * 70)
    if not test_model_loading():
        all_good = False
    
    print("\n" + "=" * 70)
    if all_good and not (missing_deps or missing_data or missing_scripts):
        print("✓ ALL CHECKS PASSED - Package is ready to use!")
        print("=" * 70)
        return 0
    else:
        print("⚠ SOME CHECKS FAILED - See details above")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())

"""
Validate trained models on uncontaminated dataset.

This script:
1. Loads trained models (from main dataset)
2. Loads AutoSpearman-selected features
3. Loads Understand reports from uncontaminated data
4. Performs intersection filter (files successfully analyzed for all LLMs)
5. Makes predictions using the same features
6. Compares performance to main dataset
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.metrics import (
    roc_auc_score, precision_score, recall_score,
    f1_score, matthews_corrcoef, confusion_matrix
)

def load_trained_model_and_features(llm, granularity):
    """Load the trained model and its selected features."""

    model_path = f"../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl"
    features_path = f"../results/selected_features_{granularity}_{llm}_intersection.csv"

    print(f"\nLoading model and features for {llm} ({granularity}-level)...")

    # Load model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f"  ✓ Model loaded from: {model_path}")

    # Load selected features
    features_df = pd.read_csv(features_path)
    selected_features = features_df['feature'].tolist()
    print(f"  ✓ Loaded {len(selected_features)} selected features")

    return model, selected_features

def load_understand_reports(granularity, base_path="../data/features_for_ML/uncontaminated"):
    """Load Understand reports for all LLMs and human."""

    print(f"\n{'='*80}")
    print(f"LOADING UNDERSTAND REPORTS ({granularity.upper()}-LEVEL)")
    print(f"{'='*80}")

    llms = ['human', 'claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
    reports = {}

    for llm in llms:
        report_path = Path(base_path) / granularity / llm / f"{llm}.csv"

        if not report_path.exists():
            print(f"  ⚠️  Report not found: {report_path}")
            continue

        df = pd.read_csv(report_path, low_memory=False)

        # Extract file ID from 'Name' column (e.g., "1.py" -> 1)
        # Remove .py extension and convert to numeric, coercing errors to NaN
        df['file_id'] = pd.to_numeric(df['Name'].str.replace('.py', '', regex=False), errors='coerce')

        # Drop rows where file_id couldn't be extracted (NaN)
        before_count = len(df)
        df = df.dropna(subset=['file_id'])
        df['file_id'] = df['file_id'].astype(int)
        after_count = len(df)

        if before_count != after_count:
            print(f"  {llm:20s}: {after_count:4d} files analyzed ({before_count - after_count} invalid filenames dropped)")
        else:
            print(f"  {llm:20s}: {after_count:4d} files analyzed")

        reports[llm] = df

    return reports

def perform_intersection_filter(reports, granularity):
    """
    Find intersection: files successfully analyzed for ALL LLMs + human.

    Returns:
        intersection_ids: Set of file IDs present in all reports
    """

    print(f"\n{'='*80}")
    print(f"INTERSECTION FILTER ({granularity.upper()}-LEVEL)")
    print(f"{'='*80}")

    # Get file IDs for each dataset
    file_ids = {}
    for llm, df in reports.items():
        file_ids[llm] = set(df['file_id'].values)
        print(f"  {llm:20s}: {len(file_ids[llm]):4d} valid file IDs")

    # Find intersection
    intersection_ids = file_ids['human']
    for llm in ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
        intersection_ids = intersection_ids.intersection(file_ids[llm])

    print(f"\n  INTERSECTION: {len(intersection_ids)} files present in ALL datasets")

    # Expected counts
    expected = {'function': 840, 'class': 554}
    retention = len(intersection_ids) / expected[granularity] * 100
    print(f"  Original: {expected[granularity]}")
    print(f"  Retention: {retention:.1f}%")

    return intersection_ids

def prepare_test_data(reports, intersection_ids, selected_features):
    """
    Prepare test data from intersection-filtered Understand reports.

    CRITICAL: Features must be in exact same order as training data!

    Returns:
        X_test: Feature matrix
        y_test: Labels (0=human, 1=LLM)
        llm_name: Which LLM this is for
    """

    print(f"\n{'='*80}")
    print(f"PREPARING TEST DATA")
    print(f"{'='*80}")

    # Metadata columns to exclude
    metadata_cols = ['Kind', 'Name', 'File', 'BaseFile', 'file_id']

    # Filter to intersection and selected features
    human_df = reports['human'][reports['human']['file_id'].isin(intersection_ids)].copy()
    human_df = human_df.sort_values('file_id').reset_index(drop=True)

    # Identify LLM dataset (there should be 4 LLMs, we'll process each separately)
    llm_dfs = {}
    for llm in ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
        llm_df = reports[llm][reports[llm]['file_id'].isin(intersection_ids)].copy()
        llm_df = llm_df.sort_values('file_id').reset_index(drop=True)

        # Verify alignment
        if not np.array_equal(human_df['file_id'].values, llm_df['file_id'].values):
            raise ValueError(f"File IDs don't align for {llm}!")

        llm_dfs[llm] = llm_df

    print(f"  Human samples: {len(human_df)}")
    for llm in llm_dfs:
        print(f"  {llm} samples: {len(llm_dfs[llm])}")

    # Check if all selected features are available
    available_features = [col for col in human_df.columns if col not in metadata_cols]
    missing_features = set(selected_features) - set(available_features)

    if missing_features:
        print(f"\n  ⚠️  WARNING: {len(missing_features)} features not found in Understand reports:")
        for feat in sorted(missing_features):
            print(f"    - {feat}")

        # Use only available features (but keep the order from selected_features!)
        selected_features = [f for f in selected_features if f in available_features]
        print(f"  Using {len(selected_features)} available features")

    # CRITICAL: Extract features in the EXACT ORDER as selected_features
    # This ensures feature order matches training data
    human_features = human_df[selected_features].copy()

    # Handle missing values (consistent with training)
    # Replace inf with NaN
    human_features = human_features.replace([np.inf, -np.inf], np.nan)

    # Check for NaN columns
    nan_cols = human_features.columns[human_features.isna().any()].tolist()
    if nan_cols:
        print(f"\n  ⚠️  WARNING: {len(nan_cols)} columns have NaN values: {nan_cols}")
        print(f"  Filling NaN with 0 to maintain feature count...")
        human_features = human_features.fillna(0)

    # Check for constant columns but DON'T drop them - model was trained with them!
    constant_cols = human_features.columns[human_features.std() == 0].tolist()
    if constant_cols:
        print(f"\n  ℹ️  Note: {len(constant_cols)} constant columns (std=0) detected: {constant_cols}")
        print(f"  Keeping them - model was trained with these features")

    print(f"\n  Final feature count: {len(selected_features)}")

    # Verify we still have features to work with
    if len(selected_features) == 0:
        raise ValueError("No features remaining after preprocessing!")

    print(f"  Feature order preserved from training data ✓")

    # Return data for each LLM separately
    test_datasets = {}
    for llm, llm_df in llm_dfs.items():
        # CRITICAL: Use selected_features list to maintain exact order
        llm_features = llm_df[selected_features].copy()

        # Same preprocessing as human
        llm_features = llm_features.replace([np.inf, -np.inf], np.nan)
        llm_features = llm_features.fillna(0)  # Fill NaN with 0, same as human
        # Do NOT drop constant columns - model expects them!

        # Verify feature order matches
        if list(human_features.columns) != list(llm_features.columns):
            raise ValueError(f"Feature order mismatch for {llm}!")

        # Combine human + LLM
        X_human = human_features.copy()
        X_human['label'] = 0

        X_llm = llm_features.copy()
        X_llm['label'] = 1

        combined = pd.concat([X_human, X_llm], ignore_index=True)

        X_test = combined.drop(columns=['label'])
        y_test = combined['label'].values

        test_datasets[llm] = {
            'X_test': X_test,
            'y_test': y_test,
            'n_features': X_test.shape[1]
        }

    return test_datasets, selected_features

def evaluate_model(model, X_test, y_test, llm_name, granularity):
    """Evaluate model on test data and return metrics."""

    print(f"\n{'='*80}")
    print(f"EVALUATING {llm_name.upper()} ({granularity.upper()}-LEVEL)")
    print(f"{'='*80}")

    # Get predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        'llm': llm_name,
        'granularity': granularity,
        'n_samples': len(y_test),
        'n_features': X_test.shape[1],
        'auc': roc_auc_score(y_test, y_pred_proba),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
        'mcc': matthews_corrcoef(y_test, y_pred)
    }

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print(f"\nConfusion Matrix:")
    print(f"  (TP, FP) = ({tp}, {fp})")
    print(f"  (FN, TN) = ({fn}, {tn})")

    print(f"\nPerformance Metrics:")
    print(f"  AUC:       {metrics['auc']:.4f}")
    print(f"  F1:        {metrics['f1']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  MCC:       {metrics['mcc']:.4f}")

    return metrics

def load_main_dataset_metrics(llm, granularity):
    """Load bootstrap metrics from main dataset for comparison."""

    bootstrap_file = f"../results/bootstrap_results_{granularity}_{llm}_intersection.csv"

    if not Path(bootstrap_file).exists():
        print(f"  ⚠️  Main dataset metrics not found: {bootstrap_file}")
        return None

    df = pd.read_csv(bootstrap_file)

    # Convert to dictionary
    metrics = {}
    for _, row in df.iterrows():
        metrics[row['metric']] = {
            'mean': row['mean'],
            'ci_lower': row['ci_lower'],
            'ci_upper': row['ci_upper']
        }

    return metrics

def compare_with_main_dataset(uncontam_metrics, main_metrics):
    """Compare uncontaminated performance with main dataset."""

    if main_metrics is None:
        return

    print(f"\n{'='*80}")
    print(f"COMPARISON: UNCONTAMINATED vs MAIN DATASET")
    print(f"{'='*80}")
    print(f"{'Metric':<12} {'Main (Mean)':>12} {'Main 95% CI':>25} {'Uncontam':>12} {'Diff':>10}")
    print("-"*80)

    for metric in ['auc', 'f1', 'precision', 'recall', 'mcc']:
        main_mean = main_metrics[metric]['mean']
        main_ci = f"[{main_metrics[metric]['ci_lower']:.4f}-{main_metrics[metric]['ci_upper']:.4f}]"
        uncontam_val = uncontam_metrics[metric]
        diff = uncontam_val - main_mean

        # Check if uncontaminated falls within CI
        in_ci = main_metrics[metric]['ci_lower'] <= uncontam_val <= main_metrics[metric]['ci_upper']
        ci_marker = "✓" if in_ci else "✗"

        print(f"{metric.upper():<12} {main_mean:>12.4f} {main_ci:>25} {uncontam_val:>12.4f} {diff:>+10.4f} {ci_marker}")

def main():
    """Main execution."""

    print("="*80)
    print("VALIDATION ON UNCONTAMINATED DATASET")
    print("="*80)

    granularities = ['function', 'class']
    llms = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']

    all_results = []

    for granularity in granularities:
        print(f"\n\n{'#'*80}")
        print(f"# PROCESSING {granularity.upper()}-LEVEL")
        print(f"{'#'*80}")

        # Load Understand reports
        reports = load_understand_reports(granularity)

        if len(reports) < 5:
            print(f"  ⚠️  Insufficient reports for {granularity}-level, skipping...")
            continue

        # Perform intersection filter
        intersection_ids = perform_intersection_filter(reports, granularity)

        if len(intersection_ids) == 0:
            print(f"  ⚠️  No intersection found for {granularity}-level, skipping...")
            continue

        # Process each LLM
        for llm in llms:
            print(f"\n{'='*80}")
            print(f"PROCESSING: {llm.upper()}")
            print(f"{'='*80}")

            # Load trained model and selected features
            model, selected_features = load_trained_model_and_features(llm, granularity)

            # Prepare test data with intersection filter
            test_datasets, final_features = prepare_test_data(reports, intersection_ids, selected_features)

            # Get this LLM's test data
            if llm not in test_datasets:
                print(f"  ⚠️  No test data for {llm}, skipping...")
                continue

            X_test = test_datasets[llm]['X_test']
            y_test = test_datasets[llm]['y_test']

            # Evaluate model
            uncontam_metrics = evaluate_model(model, X_test, y_test, llm, granularity)

            # Load main dataset metrics
            main_metrics = load_main_dataset_metrics(llm, granularity)

            # Compare
            compare_with_main_dataset(uncontam_metrics, main_metrics)

            # Store results
            all_results.append(uncontam_metrics)

    # Save all results
    print(f"\n\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")

    results_df = pd.DataFrame(all_results)
    output_file = "../results/uncontaminated_validation_results.csv"
    results_df.to_csv(output_file, index=False)

    print(f"\n✓ Results saved to: {output_file}")

    # Summary table
    print(f"\n{'='*80}")
    print("SUMMARY: UNCONTAMINATED VALIDATION")
    print(f"{'='*80}")
    print(results_df.to_string(index=False))

    print(f"\n{'='*80}")
    print("COMPLETE!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
"""
DeLong's Test for AUC Comparison
Compares detection performance across LLMs using DeLong's test
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from sklearn.metrics import roc_auc_score
import pickle
import warnings
warnings.filterwarnings('ignore')

def compute_midrank(x):
    """Computes midranks"""
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=np.float64)
    i = 0

    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1)
        i = j

    T2 = np.empty(N, dtype=np.float64)
    T2[J] = T + 1

    return T2

def fastDeLong(predictions_sorted_transposed, label_1_count):
    """Fast DeLong implementation"""
    m = label_1_count
    n = predictions_sorted_transposed.shape[1] - m
    positive_examples = predictions_sorted_transposed[:, :m]
    negative_examples = predictions_sorted_transposed[:, m:]
    k = predictions_sorted_transposed.shape[0]

    tx = np.empty([k, m], dtype=np.float64)
    ty = np.empty([k, n], dtype=np.float64)
    tz = np.empty([k, m + n], dtype=np.float64)

    for r in range(k):
        tx[r, :] = compute_midrank(positive_examples[r, :])
        ty[r, :] = compute_midrank(negative_examples[r, :])
        tz[r, :] = compute_midrank(predictions_sorted_transposed[r, :])

    aucs = tz[:, :m].sum(axis=1) / m / n - float(m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx[:, :]) / n
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    delongcov = sx / m + sy / n

    return aucs, delongcov

def delong_roc_test(ground_truth, predictions_1, predictions_2):
    """
    Compares two ROC curves using DeLong's test
    Returns: z-statistic, p-value, AUC1, AUC2
    """
    # Ensure same test set
    if len(ground_truth) != len(predictions_1) or len(ground_truth) != len(predictions_2):
        raise ValueError("All arrays must have same length")

    auc_1 = roc_auc_score(ground_truth, predictions_1)
    auc_2 = roc_auc_score(ground_truth, predictions_2)

    # Stack predictions
    predictions_stacked = np.vstack([predictions_1, predictions_2])

    order = np.argsort(ground_truth)[::-1]
    label_1_count = np.sum(ground_truth == 1)

    predictions_sorted_transposed = predictions_stacked[:, order]

    aucs, delongcov = fastDeLong(predictions_sorted_transposed, int(label_1_count))

    # Compute z-statistic
    z = (auc_1 - auc_2) / np.sqrt(delongcov[0, 0] + delongcov[1, 1] - 2 * delongcov[0, 1])

    # Two-tailed p-value
    p_value = 2 * (1 - norm.cdf(abs(z)))

    return z, p_value, auc_1, auc_2

def main():
    # Configuration
    models = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
    granularities = ['function', 'class']

    # Paths
    test_data_path = "../data/data_for_ML_validation"
    model_path = "../data/trained_ML_models"

    print("="*80)
    print("DELONG'S TEST FOR AUC COMPARISON")
    print("="*80)
    print("Loading trained models and generating predictions...")
    print()

    # Store predictions for each configuration
    all_predictions = {}

    for granularity in granularities:
        print(f"\n{granularity.upper()}-LEVEL:")
        print("-" * 80)

        for model in models:
            # Load test data with labels
            test_file = f"{test_data_path}/{model}_{granularity}_test_data_intersection.csv"
            test_df = pd.read_csv(test_file)

            # Load trained model
            model_file = f"{model_path}/{granularity}_{model}_finalized_model_intersection.pkl"
            with open(model_file, 'rb') as f:
                clf = pickle.load(f)

            # Separate features and labels
            X_test = test_df.drop('label', axis=1)
            y_test = test_df['label'].values

            # Get predictions (probabilities for class 1 = LLM)
            y_pred_proba = clf.predict_proba(X_test)[:, 1]

            # Store
            key = f"{model}_{granularity}"
            all_predictions[key] = {
                'y_true': y_test,
                'y_pred': y_pred_proba,
                'auc': roc_auc_score(y_test, y_pred_proba)
            }

            print(f"  {model:<20} AUC: {all_predictions[key]['auc']:.4f} (n={len(y_test)})")

    # Now run DeLong's test for all pairwise comparisons
    print("\n" + "="*80)
    print("DELONG'S TEST RESULTS: PAIRWISE AUC COMPARISONS")
    print("="*80)

    results = []

    for granularity in granularities:
        print(f"\n{granularity.upper()}-LEVEL COMPARISONS:")
        print("-" * 80)
        print(f"{'Comparison':<45} {'AUC Diff':>10} {'Z-statistic':>12} {'P-value':>10} {'Significant':>12}")
        print("-" * 80)

        # Sort models by AUC for this granularity
        model_aucs = [(m, all_predictions[f"{m}_{granularity}"]['auc']) for m in models]
        model_aucs.sort(key=lambda x: x[1], reverse=True)

        # Store comparisons for this granularity
        gran_comparisons = []

        # Compare all pairs
        for i in range(len(model_aucs)):
            for j in range(i+1, len(model_aucs)):
                model1, auc1 = model_aucs[i]
                model2, auc2 = model_aucs[j]

                key1 = f"{model1}_{granularity}"
                key2 = f"{model2}_{granularity}"

                # Get predictions and true labels
                y_true = all_predictions[key1]['y_true']  # Same for both (intersection)
                y_pred1 = all_predictions[key1]['y_pred']
                y_pred2 = all_predictions[key2]['y_pred']

                # Run DeLong's test
                z, p_value, _, _ = delong_roc_test(y_true, y_pred1, y_pred2)

                auc_diff = auc1 - auc2

                gran_comparisons.append({
                    'model1': model1,
                    'model2': model2,
                    'auc_diff': auc_diff,
                    'z_statistic': z,
                    'p_value': p_value
                })

        # Apply Bonferroni correction within this granularity
        n_comparisons = len(gran_comparisons)
        bonferroni_alpha = 0.05 / n_comparisons

        print(f"\nBonferroni correction: α = 0.05/{n_comparisons} = {bonferroni_alpha:.4f}")
        print("-" * 80)

        # Print results with corrected significance
        for comp in gran_comparisons:
            comparison = f"{comp['model1']} vs {comp['model2']}"
            p_val = comp['p_value']

            # Determine significance with correction
            if p_val < 0.001:
                sig = "YES (p<0.001)"
            elif p_val < bonferroni_alpha:
                sig = f"YES (p<{bonferroni_alpha:.4f})"
            elif p_val < 0.05:
                sig = "MARGINAL (ns after correction)"
            else:
                sig = "NO"

            print(f"{comparison:<45} {comp['auc_diff']:>10.4f} {comp['z_statistic']:>12.4f} {p_val:>10.6f} {sig:>12}")

            # Store results with corrected significance
            results.append({
                'granularity': granularity,
                'model1': comp['model1'],
                'model2': comp['model2'],
                'auc1': all_predictions[f"{comp['model1']}_{granularity}"]['auc'],
                'auc2': all_predictions[f"{comp['model2']}_{granularity}"]['auc'],
                'auc_diff': comp['auc_diff'],
                'z_statistic': comp['z_statistic'],
                'p_value': p_val,
                'significant_uncorrected': p_val < 0.05,
                'significant_bonferroni': p_val < bonferroni_alpha,
                'bonferroni_alpha': bonferroni_alpha
            })

        # Summary for this granularity
        n_sig_uncorrected = sum([c['p_value'] < 0.05 for c in gran_comparisons])
        n_sig_corrected = sum([c['p_value'] < bonferroni_alpha for c in gran_comparisons])

        print(f"\nSummary:")
        print(f"  Significant (uncorrected α=0.05): {n_sig_uncorrected}/{n_comparisons}")
        print(f"  Significant (Bonferroni α={bonferroni_alpha:.4f}): {n_sig_corrected}/{n_comparisons}")

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('../results/delong_test_results_intersection.csv', index=False)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    # Overall summary
    results_df = pd.DataFrame(results)
    total_tests = len(results_df)
    sig_uncorrected = sum(results_df['significant_uncorrected'])
    sig_bonferroni = sum(results_df['significant_bonferroni'])

    print(f"Total comparisons: {total_tests}")
    print(f"Significant (uncorrected α=0.05): {sig_uncorrected}/{total_tests}")
    print(f"Significant (Bonferroni-corrected): {sig_bonferroni}/{total_tests}")
    print()

    # Per-granularity summary
    for gran in ['function', 'class']:
        gran_df = results_df[results_df['granularity'] == gran]
        n_tests = len(gran_df)
        bonf_alpha = gran_df.iloc[0]['bonferroni_alpha']
        n_sig_uncorr = sum(gran_df['significant_uncorrected'])
        n_sig_bonf = sum(gran_df['significant_bonferroni'])

        print(f"{gran.capitalize()}-level ({n_tests} tests, Bonferroni α={bonf_alpha:.4f}):")
        print(f"  Uncorrected: {n_sig_uncorr}/{n_tests} significant")
        print(f"  Bonferroni:  {n_sig_bonf}/{n_tests} significant")

    print()
    print(f"Results saved to: delong_test_results_intersection.csv")
    print()
    print("INTERPRETATION:")
    print("- Multiple comparison correction applied per granularity (Bonferroni)")
    print("- Function and class treated as separate families of tests")
    print("- Z-statistic: Standardized difference between AUCs")
    print("- P-value < Bonferroni α: Statistically significant after correction")
    print("- DeLong's test accounts for correlation (same test set)")
    print("="*80)

if __name__ == "__main__":
    main()
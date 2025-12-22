"""
RQ1: Statistical Analysis - LLM vs Human Code Characteristics
Performs Mann-Whitney U test with Cliff's Delta effect size
Includes Holm-Bonferroni correction for multiple comparisons

UPDATED: Uses global intersection data for fair cross-model comparison
"""

import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

# Feature lists for each granularity
FUNCTION_FEATURES = [
    'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl',
    'CountLineCodeExe', 'CountLineComment', 'CountPath', 'CountPathLog',
    'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'Cyclomatic',
    'CyclomaticModified', 'CyclomaticStrict', 'CyclomaticStrictModified',
    'Essential', 'MaxNesting', 'RatioCommentToCode'
]

CLASS_FEATURES = [
    'AvgCountLine', 'AvgCountLineBlank', 'AvgCountLineCode', 'AvgCountLineComment',
    'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict',
    'AvgCyclomaticStrictModified', 'AvgEssential', 'CountClassBase',
    'CountClassCoupled', 'CountClassCoupledModified', 'CountClassDerived',
    'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod',
    'CountDeclMethodAll', 'CountLine', 'CountLineBlank', 'CountLineCode',
    'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountStmt',
    'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxCyclomaticModified',
    'MaxCyclomaticStrict', 'MaxCyclomaticStrictModified', 'MaxEssential',
    'MaxInheritanceTree', 'MaxNesting', 'RatioCommentToCode', 'SumCyclomatic',
    'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumCyclomaticStrictModified',
    'SumEssential'
]

# Mapping of API IDs to full names for display
FEATURE_NAMES = {
    'AvgCountLine': 'Average Lines',
    'AvgCountLineBlank': 'Average Blank Lines',
    'AvgCountLineCode': 'Average Code Lines',
    'AvgCountLineComment': 'Average Comment Lines',
    'AvgCyclomatic': 'Average Cyclomatic Complexity',
    'AvgCyclomaticModified': 'Average Modified Cyclomatic Complexity',
    'AvgCyclomaticStrict': 'Average Strict Cyclomatic Complexity',
    'AvgCyclomaticStrictModified': 'Average Strict Modified Cyclomatic Complexity',
    'AvgEssential': 'Average Essential Complexity',
    'CountClassBase': 'Base Classes',
    'CountClassCoupled': 'Coupled Classes',
    'CountClassCoupledModified': 'Coupled Classes Modified',
    'CountClassDerived': 'Derived Classes',
    'CountDeclInstanceMethod': 'Instance Methods',
    'CountDeclInstanceVariable': 'Instance Variables',
    'CountDeclMethod': 'Methods',
    'CountDeclMethodAll': 'All Methods',
    'CountLine': 'Lines',
    'CountLineBlank': 'Blank Lines',
    'CountLineCode': 'Code Lines',
    'CountLineCodeDecl': 'Declarative Code Lines',
    'CountLineCodeExe': 'Executable Code Lines',
    'CountLineComment': 'Comment Lines',
    'CountPath': 'Paths',
    'CountPathLog': 'Paths Log(x)',
    'CountStmt': 'Statements',
    'CountStmtDecl': 'Declarative Statements',
    'CountStmtExe': 'Executable Statements',
    'Cyclomatic': 'Cyclomatic Complexity',
    'CyclomaticModified': 'Modified Cyclomatic Complexity',
    'CyclomaticStrict': 'Strict Cyclomatic Complexity',
    'CyclomaticStrictModified': 'Strict Modified Cyclomatic Complexity',
    'Essential': 'Essential Complexity',
    'MaxCyclomatic': 'Max Cyclomatic Complexity',
    'MaxCyclomaticModified': 'Max Modified Cyclomatic Complexity',
    'MaxCyclomaticStrict': 'Max Strict Cyclomatic Complexity',
    'MaxCyclomaticStrictModified': 'Max Strict Modified Cyclomatic Complexity',
    'MaxEssential': 'Max Essential Complexity',
    'MaxInheritanceTree': 'Max Inheritance Tree',
    'MaxNesting': 'Max Nesting',
    'RatioCommentToCode': 'Comment to Code Ratio',
    'SumCyclomatic': 'Sum Cyclomatic Complexity',
    'SumCyclomaticModified': 'Sum Modified Cyclomatic Complexity',
    'SumCyclomaticStrict': 'Sum Strict Cyclomatic Complexity',
    'SumCyclomaticStrictModified': 'Sum Strict Modified Cyclomatic Complexity',
    'SumEssential': 'Sum Essential Complexity'
}

def cliffs_delta(group1, group2):
    """
    Calculate Cliff's Delta effect size
    Returns: delta value and magnitude category
    """
    n1, n2 = len(group1), len(group2)

    # Calculate number of pairs where group1 > group2 and group1 < group2
    dominance = 0
    for val1 in group1:
        for val2 in group2:
            if val1 > val2:
                dominance += 1
            elif val1 < val2:
                dominance -= 1

    delta = dominance / (n1 * n2)

    # Categorize effect size
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        magnitude = "Negligible"
    elif abs_delta < 0.33:
        magnitude = "Small"
    elif abs_delta < 0.474:
        magnitude = "Medium"
    else:
        magnitude = "Large"

    return delta, magnitude

def holm_bonferroni_correction(p_values, alpha=0.01):
    """
    Apply Holm-Bonferroni correction for multiple comparisons

    Args:
        p_values: list of p-values
        alpha: significance level (default 0.01)

    Returns:
        list of booleans indicating significance after correction
    """
    n = len(p_values)

    # Create array of (index, p_value) and sort by p_value
    indexed_p_values = [(i, p) for i, p in enumerate(p_values)]
    indexed_p_values.sort(key=lambda x: x[1])

    # Initialize significance array
    is_significant = [False] * n

    # Apply Holm-Bonferroni sequential testing
    for rank, (idx, p_val) in enumerate(indexed_p_values, start=1):
        adjusted_alpha = alpha / (n - rank + 1)
        if p_val <= adjusted_alpha:
            is_significant[idx] = True
        else:
            # Once we fail to reject, all subsequent tests also fail
            break

    return is_significant

def load_intersection_data(human_file, llm_file, granularity, features):
    """
    Load intersection data - already aligned and matched

    Args:
        human_file: path to human intersection CSV
        llm_file: path to LLM intersection CSV
        granularity: 'function' or 'class'
        features: list of feature columns to keep

    Returns:
        tuple of (human_data, llm_data) DataFrames
    """
    # Load data
    human_df = pd.read_csv(human_file)
    llm_df = pd.read_csv(llm_file)

    print(f"  Loaded {len(human_df)} matched snippets from intersection")

    # Verify alignment
    if len(human_df) != len(llm_df):
        raise ValueError(f"Mismatched lengths: human={len(human_df)}, llm={len(llm_df)}")

    # Verify composite keys match (they should be pre-aligned)
    if 'composite_key' in human_df.columns and 'composite_key' in llm_df.columns:
        if list(human_df['composite_key']) != list(llm_df['composite_key']):
            raise ValueError("Composite keys don't match - data not properly aligned!")

    # Extract feature columns
    human_data = human_df[features].copy()
    llm_data = llm_df[features].copy()

    return human_data, llm_data

def analyze_feature_differences(human_data, llm_data, llm_name, granularity, feature_name):
    """
    Perform Mann-Whitney U test and calculate Cliff's Delta for a single feature

    Args:
        human_data: array of human-written code feature values
        llm_data: array of LLM-generated code feature values
        llm_name: name of the LLM
        granularity: 'function' or 'class'
        feature_name: name of the feature being analyzed

    Returns:
        dict with test results
    """
    # Mann-Whitney U test
    statistic, p_value = mannwhitneyu(human_data, llm_data, alternative='two-sided')

    # Cliff's Delta
    delta, magnitude = cliffs_delta(llm_data, human_data)

    # Determine direction
    direction = "↑" if np.median(llm_data) > np.median(human_data) else "↓"

    # Get full feature name for display
    feature_full_name = FEATURE_NAMES.get(feature_name, feature_name)

    return {
        'llm': llm_name,
        'granularity': granularity,
        'feature': feature_name,
        'feature_full_name': feature_full_name,
        'p_value': p_value,
        'cliff_delta': delta,
        'effect_size': magnitude,
        'direction': direction,
        'human_median': np.median(human_data),
        'llm_median': np.median(llm_data),
        'human_mean': np.mean(human_data),
        'llm_mean': np.mean(llm_data)
    }

def main():
    """
    Main analysis function
    """
    # Define models and granularities
    models = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
    granularities = ['function', 'class']

    # Base data path - NOW USING INTERSECTION DATA
    data_path = "../data/features_for_ML"

    all_results = []

    print("=" * 80)
    print("RQ1: Statistical Analysis - LLM vs Human Code Characteristics")
    print("Using Global Intersection Data for Fair Cross-Model Comparison")
    print("=" * 80)
    print(f"\nPerforming Mann-Whitney U tests with Holm-Bonferroni correction")
    print(f"Significance level: α = 0.01")
    print(f"Function-level features: {len(FUNCTION_FEATURES)}")
    print(f"Class-level features: {len(CLASS_FEATURES)}")
    print(f"Total configurations: {len(models) * len(granularities)}")
    print(f"\nNote: Using intersection data (same prompts across all LLMs)")
    print("=" * 80)

    # Perform analysis for each configuration
    for granularity in granularities:
        features = FUNCTION_FEATURES if granularity == 'function' else CLASS_FEATURES

        for model in models:
            print(f"\n### Analyzing {model} ({granularity}-level) ###")

            # Construct file paths - USE INTERSECTION DATA
            human_file = f"{data_path}/{granularity}_global_intersection/human/human_intersection.csv"
            llm_file = f"{data_path}/{granularity}_global_intersection/{model}/{model}_intersection.csv"

            try:
                # Load intersection data (already aligned)
                human_df, llm_df = load_intersection_data(
                    human_file, llm_file, granularity, features
                )

            except FileNotFoundError as e:
                print(f"  ⚠️  Data files not found: {e}")
                continue
            except Exception as e:
                print(f"  ⚠️  Error loading data: {e}")
                continue

            config_results = []

            # Test each feature
            for feature in features:
                if feature not in human_df.columns or feature not in llm_df.columns:
                    print(f"  ⚠️  Feature {feature} not found in data")
                    continue

                # Remove NaN values
                human_vals = human_df[feature].dropna().values
                llm_vals = llm_df[feature].dropna().values

                if len(human_vals) == 0 or len(llm_vals) == 0:
                    print(f"  ⚠️  No valid data for feature {feature}")
                    continue

                result = analyze_feature_differences(
                    human_vals,
                    llm_vals,
                    model,
                    granularity,
                    feature
                )
                config_results.append(result)

            # Apply Holm-Bonferroni correction
            p_values = [r['p_value'] for r in config_results]
            is_significant = holm_bonferroni_correction(p_values, alpha=0.01)

            # Add corrected significance to results
            for i, result in enumerate(config_results):
                result['significant_corrected'] = is_significant[i]
                result['significant_uncorrected'] = result['p_value'] < 0.01
                all_results.append(result)

            # Print summary for this configuration
            sig_count = sum(is_significant)
            sig_with_effect = sum([
                1 for i, sig in enumerate(is_significant)
                if sig and config_results[i]['effect_size'] != 'Negligible'
            ])
            print(f"  Significant features (after correction): {sig_count}/{len(features)}")
            print(f"  Significant with non-negligible effect: {sig_with_effect}/{len(features)}")

    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)

    # Save detailed results
    results_df.to_csv('../results/rq1_statistical_results_detailed_intersection.csv', index=False)
    print(f"\n✓ Detailed results saved to: rq1_statistical_results_detailed_intersection.csv")

    # Create summary tables for paper
    create_summary_tables(results_df, models, granularities)

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)

def create_summary_tables(results_df, models, granularities):
    """
    Create summary tables for the paper
    """
    print("\n### Creating Summary Tables ###")

    # Table 1: Count of significant features per configuration
    summary_counts = []
    for gran in granularities:
        gran_features = FUNCTION_FEATURES if gran == 'function' else CLASS_FEATURES

        for model in models:
            config_data = results_df[
                (results_df['llm'] == model) &
                (results_df['granularity'] == gran)
            ]

            if len(config_data) == 0:
                continue

            sig_count = config_data['significant_corrected'].sum()
            sig_with_effect = config_data[
                (config_data['significant_corrected'] == True) &
                (config_data['effect_size'] != 'Negligible')
            ].shape[0]

            summary_counts.append({
                'Model': model,
                'Granularity': gran,
                'Total Features': len(gran_features),
                'Significant (corrected)': sig_count,
                'Significant + Non-Negligible': sig_with_effect
            })

    summary_df = pd.DataFrame(summary_counts)
    summary_df.to_csv('../results/rq1_summary_counts_intersection.csv', index=False)
    print("✓ Summary counts saved to: rq1_summary_counts_intersection.csv")
    print("\n" + summary_df.to_string(index=False))

    # Table 2: Features with consistent patterns across models
    print("\n### Features with Consistent Patterns ###")

    for gran in granularities:
        gran_features = FUNCTION_FEATURES if gran == 'function' else CLASS_FEATURES
        print(f"\n{gran.capitalize()}-level:")

        for feature in gran_features:
            feature_data = results_df[
                (results_df['feature'] == feature) &
                (results_df['granularity'] == gran)
            ]

            if len(feature_data) == 0:
                continue

            sig_count = feature_data['significant_corrected'].sum()

            if sig_count >= 3:  # Significant in at least 75% of models
                feature_name = FEATURE_NAMES.get(feature, feature)
                print(f"\n  {feature_name}: Significant in {sig_count}/4 models")

                # Show direction and effect size for each model
                for _, row in feature_data.iterrows():
                    if row['significant_corrected']:
                        print(f"    {row['llm']}: {row['effect_size']} effect, {row['direction']}")

if __name__ == "__main__":
    main()
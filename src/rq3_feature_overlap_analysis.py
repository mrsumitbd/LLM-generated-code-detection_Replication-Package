# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import warnings
# import os
#
# warnings.filterwarnings('ignore')
#
# # Set style
# sns.set_style("whitegrid")
# plt.rcParams['figure.figsize'] = (14, 8)
# plt.rcParams['font.size'] = 11
#
# print('=' * 80)
# print('RQ3: FEATURE OVERLAP AND GENERALIZATION PATTERN ANALYSIS')
# print('USING INTERSECTION DATA')
# print('=' * 80)
#
# # ============================================================
# # Load AutoSpearman Selected Features
# # ============================================================
#
# print('\nLoading AutoSpearman selected features from intersection data...')
#
# # Model mapping
# model_mapping = {
#     'claude-3-haiku': 'Claude 3 Haiku',
#     'claude-4-5-haiku': 'Claude 4.5 Haiku',
#     'gpt-3-5': 'GPT-3.5',
#     'gpt-oss': 'GPT-OSS'
# }
#
# # Load selected features for each configuration
# selected_features = {}
#
# for llm in ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
#     for granularity in ['Function', 'Class']:
#         config_key = f'{llm}_{granularity}'
#
#         # Try to load from test data (features are the columns minus 'label')
#         try:
#             test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
#             features = [col for col in test_data.columns if col != 'label']
#             selected_features[config_key] = set(features)
#             print(f'✓ Loaded {len(features)} features for {model_mapping[llm]} {granularity}')
#         except FileNotFoundError:
#             print(f'✗ Could not find test data for {llm} {granularity}')
#             selected_features[config_key] = set()
#
#
# # ============================================================
# # Jaccard Similarity Analysis
# # ============================================================
#
# def jaccard_similarity(set1, set2):
#     """Calculate Jaccard similarity coefficient."""
#     if len(set1) == 0 and len(set2) == 0:
#         return 1.0
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#     return intersection / union if union > 0 else 0.0
#
#
# def interpret_jaccard(j):
#     """Interpret Jaccard similarity."""
#     if j >= 0.8:
#         return "Very High"
#     elif j >= 0.6:
#         return "High"
#     elif j >= 0.4:
#         return "Moderate"
#     elif j >= 0.2:
#         return "Low"
#     else:
#         return "Negligible"
#
#
# print('\n' + '=' * 80)
# print('CROSS-MODEL FEATURE OVERLAP (SAME GRANULARITY)')
# print('=' * 80)
#
# # Function-level overlap
# print('\n--- FUNCTION-LEVEL OVERLAP ---\n')
#
# llms = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
# function_overlap_matrix = pd.DataFrame(index=[model_mapping[l] for l in llms],
#                                        columns=[model_mapping[l] for l in llms])
#
# for i, llm1 in enumerate(llms):
#     for j, llm2 in enumerate(llms):
#         if i == j:
#             # Diagonal: show feature count
#             count = len(selected_features[f'{llm1}_Function'])
#             function_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"({count})"
#         else:
#             # Off-diagonal: Jaccard similarity
#             jaccard = jaccard_similarity(
#                 selected_features[f'{llm1}_Function'],
#                 selected_features[f'{llm2}_Function']
#             )
#             function_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"{jaccard:.3f}"
#
# print('Function-level Jaccard Similarity Matrix:')
# print(function_overlap_matrix)
#
# # Check if all function-level features are identical
# function_features_list = [selected_features[f'{llm}_Function'] for llm in llms]
# all_identical = all(f == function_features_list[0] for f in function_features_list)
#
# if all_identical:
#     print('\n⭐ CRITICAL FINDING: All function-level models use IDENTICAL feature sets!')
#     print(f'   Universal feature set size: {len(function_features_list[0])}')
#     print(f'   Features: {sorted(function_features_list[0])}')
# else:
#     print('\n   Function-level features vary by model')
#
# # Class-level overlap
# print('\n--- CLASS-LEVEL OVERLAP ---\n')
#
# class_overlap_matrix = pd.DataFrame(index=[model_mapping[l] for l in llms],
#                                     columns=[model_mapping[l] for l in llms])
#
# class_overlap_values = []
# for i, llm1 in enumerate(llms):
#     for j, llm2 in enumerate(llms):
#         if i == j:
#             # Diagonal: show feature count
#             count = len(selected_features[f'{llm1}_Class'])
#             class_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"({count})"
#         else:
#             # Off-diagonal: Jaccard similarity
#             jaccard = jaccard_similarity(
#                 selected_features[f'{llm1}_Class'],
#                 selected_features[f'{llm2}_Class']
#             )
#             class_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"{jaccard:.3f}"
#             if i < j:  # Only count each pair once
#                 class_overlap_values.append(jaccard)
#
# print('Class-level Jaccard Similarity Matrix:')
# print(class_overlap_matrix)
#
# print(f'\nClass-level Statistics:')
# print(f'  Average Jaccard: {np.mean(class_overlap_values):.3f}')
# print(f'  Range: [{np.min(class_overlap_values):.3f}, {np.max(class_overlap_values):.3f}]')
# print(f'  Interpretation: {interpret_jaccard(np.mean(class_overlap_values))}')
#
# # ============================================================
# # CROSS-GRANULARITY OVERLAP (WITHIN MODEL)
# # ============================================================
#
# print('\n' + '=' * 80)
# print('CROSS-GRANULARITY FEATURE OVERLAP (WITHIN MODEL)')
# print('=' * 80 + '\n')
#
# granularity_overlap = []
# for llm in llms:
#     func_features = selected_features[f'{llm}_Function']
#     class_features = selected_features[f'{llm}_Class']
#
#     jaccard = jaccard_similarity(func_features, class_features)
#     overlap = func_features.intersection(class_features)
#
#     granularity_overlap.append({
#         'Model': model_mapping[llm],
#         'Function_Features': len(func_features),
#         'Class_Features': len(class_features),
#         'Overlap_Count': len(overlap),
#         'Jaccard': jaccard,
#         'Interpretation': interpret_jaccard(jaccard)
#     })
#
#     print(f'{model_mapping[llm]:20s}:')
#     print(f'  Function features: {len(func_features)}')
#     print(f'  Class features:    {len(class_features)}')
#     print(f'  Overlap:           {len(overlap)} features')
#     print(f'  Jaccard:           {jaccard:.3f} ({interpret_jaccard(jaccard)})')
#     print(f'  Shared features:   {sorted(overlap) if overlap else "None"}')
#     print()
#
# granularity_df = pd.DataFrame(granularity_overlap)
#
# print('Summary Statistics:')
# print(f'  Average cross-granularity Jaccard: {granularity_df["Jaccard"].mean():.3f}')
# print(f'  Range: [{granularity_df["Jaccard"].min():.3f}, {granularity_df["Jaccard"].max():.3f}]')
#
# # Compare to cross-model overlap
# avg_cross_model_class = np.mean(class_overlap_values)
# avg_cross_granularity = granularity_df["Jaccard"].mean()
#
# print(f'\n⭐ KEY COMPARISON:')
# print(f'  Cross-model overlap (same granularity): {avg_cross_model_class:.3f}')
# print(f'  Cross-granularity overlap (same model): {avg_cross_granularity:.3f}')
# print(f'  Ratio: {avg_cross_model_class / avg_cross_granularity:.1f}x')
# print(
#     f'\n  → Granularity affects features {avg_cross_model_class / avg_cross_granularity:.1f}x MORE than model choice!')
#
# # ============================================================
# # UNIVERSAL FEATURES ANALYSIS
# # ============================================================
#
# print('\n' + '=' * 80)
# print('UNIVERSAL FEATURES ACROSS ALL CONFIGURATIONS')
# print('=' * 80 + '\n')
#
# # Count feature frequency across all 8 configurations
# feature_frequency = {}
# all_features = set()
#
# for config_key, features in selected_features.items():
#     all_features.update(features)
#     for feature in features:
#         feature_frequency[feature] = feature_frequency.get(feature, 0) + 1
#
# # Categorize features
# universal_features = [f for f, count in feature_frequency.items() if count == 8]
# highly_common_features = [f for f, count in feature_frequency.items() if 6 <= count < 8]
# common_features = [f for f, count in feature_frequency.items() if 4 <= count < 6]
# model_specific_features = [f for f, count in feature_frequency.items() if count < 4]
#
# print(f'Total unique features across all configurations: {len(all_features)}')
# print(f'\nFeature Categories:')
# print(f'  Universal (8/8 configs):      {len(universal_features)} features')
# print(f'  Highly Common (6-7/8):        {len(highly_common_features)} features')
# print(f'  Common (4-5/8):               {len(common_features)} features')
# print(f'  Model/Granularity-Specific:   {len(model_specific_features)} features')
#
# print(f'\n⭐ UNIVERSAL FEATURES (appear in all 8 configurations):')
# if universal_features:
#     for feature in sorted(universal_features):
#         print(f'  - {feature}')
# else:
#     print('  (None)')
#
# print(f'\nHIGHLY COMMON FEATURES (6-7/8 configurations):')
# for feature in sorted(highly_common_features):
#     count = feature_frequency[feature]
#     print(f'  - {feature:35s} ({count}/8)')
#
# # Detailed frequency table
# freq_df = pd.DataFrame([
#     {'Feature': f, 'Frequency': count, 'Percentage': f'{count / 8 * 100:.0f}%'}
#     for f, count in sorted(feature_frequency.items(), key=lambda x: (-x[1], x[0]))
# ])
#
# # ============================================================
# # VISUALIZATION 1: Heatmap of Feature Overlap
# # ============================================================
#
# print('\n' + '=' * 80)
# print('GENERATING VISUALIZATIONS')
# print('=' * 80 + '\n')
#
# os.makedirs('../plots_for_paper', exist_ok=True)
# os.makedirs('../results', exist_ok=True)
#
# # Create numerical matrices for heatmap
# func_overlap_numeric = np.zeros((4, 4))
# class_overlap_numeric = np.zeros((4, 4))
#
# for i, llm1 in enumerate(llms):
#     for j, llm2 in enumerate(llms):
#         if i == j:
#             func_overlap_numeric[i, j] = 1.0
#             class_overlap_numeric[i, j] = 1.0
#         else:
#             func_overlap_numeric[i, j] = jaccard_similarity(
#                 selected_features[f'{llm1}_Function'],
#                 selected_features[f'{llm2}_Function']
#             )
#             class_overlap_numeric[i, j] = jaccard_similarity(
#                 selected_features[f'{llm1}_Class'],
#                 selected_features[f'{llm2}_Class']
#             )
#
# fig, axes = plt.subplots(1, 2, figsize=(16, 6))
#
# # Function-level heatmap
# sns.heatmap(func_overlap_numeric, annot=True, fmt='.3f', cmap='YlOrRd',
#             xticklabels=[model_mapping[l] for l in llms],
#             yticklabels=[model_mapping[l] for l in llms],
#             vmin=0, vmax=1, cbar_kws={'label': 'Jaccard Similarity'},
#             ax=axes[0], linewidths=0.5, linecolor='gray')
# axes[0].set_title('Function-Level Feature Overlap', fontsize=14, fontweight='bold')
# axes[0].set_xlabel('Model', fontweight='bold')
# axes[0].set_ylabel('Model', fontweight='bold')
#
# # Class-level heatmap
# sns.heatmap(class_overlap_numeric, annot=True, fmt='.3f', cmap='YlOrRd',
#             xticklabels=[model_mapping[l] for l in llms],
#             yticklabels=[model_mapping[l] for l in llms],
#             vmin=0, vmax=1, cbar_kws={'label': 'Jaccard Similarity'},
#             ax=axes[1], linewidths=0.5, linecolor='gray')
# axes[1].set_title('Class-Level Feature Overlap', fontsize=14, fontweight='bold')
# axes[1].set_xlabel('Model', fontweight='bold')
# axes[1].set_ylabel('Model', fontweight='bold')
#
# plt.tight_layout()
# plt.savefig('../plots_for_paper/rq3_feature_overlap_heatmaps_intersection.pdf', dpi=300, bbox_inches='tight')
# print('✓ Saved: ../plots_for_paper/rq3_feature_overlap_heatmaps_intersection.pdf')
#
# # ============================================================
# # VISUALIZATION 2: Feature Frequency Bar Chart
# # ============================================================
#
# fig, ax = plt.subplots(figsize=(12, 8))
#
# # Get top 20 features by frequency
# top_features = freq_df.head(20)
#
# colors = ['#d62728' if row['Frequency'] == 8 else  # Universal (red)
#           '#ff7f0e' if row['Frequency'] >= 6 else  # Highly common (orange)
#           '#2ca02c' if row['Frequency'] >= 4 else  # Common (green)
#           '#1f77b4'  # Model-specific (blue)
#           for _, row in top_features.iterrows()]
#
# bars = ax.barh(range(len(top_features)), top_features['Frequency'], color=colors)
# ax.set_yticks(range(len(top_features)))
# ax.set_yticklabels(top_features['Feature'])
# ax.set_xlabel('Number of Configurations (out of 8)', fontweight='bold', fontsize=12)
# ax.set_ylabel('Feature', fontweight='bold', fontsize=12)
# ax.set_title('Top 20 Features by Frequency Across Configurations',
#              fontsize=14, fontweight='bold')
# ax.set_xlim(0, 8.5)
# ax.grid(axis='x', alpha=0.3)
#
# # Add value labels
# for i, (bar, freq) in enumerate(zip(bars, top_features['Frequency'])):
#     ax.text(freq + 0.1, i, f'{freq}/8', va='center', fontweight='bold')
#
# # Legend
# from matplotlib.patches import Patch
#
# legend_elements = [
#     Patch(facecolor='#d62728', label='Universal (8/8)'),
#     Patch(facecolor='#ff7f0e', label='Highly Common (6-7/8)'),
#     Patch(facecolor='#2ca02c', label='Common (4-5/8)'),
#     Patch(facecolor='#1f77b4', label='Model-Specific (<4/8)')
# ]
# ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
#
# plt.tight_layout()
# plt.savefig('../plots_for_paper/rq3_feature_frequency_intersection.pdf', dpi=300, bbox_inches='tight')
# print('✓ Saved: ../plots_for_paper/rq3_feature_frequency_intersection.pdf')
#
# # ============================================================
# # SAVE RESULTS TO CSV
# # ============================================================
#
# # Feature overlap matrices
# func_overlap_df = pd.DataFrame(func_overlap_numeric,
#                                index=[model_mapping[l] for l in llms],
#                                columns=[model_mapping[l] for l in llms])
# class_overlap_df = pd.DataFrame(class_overlap_numeric,
#                                 index=[model_mapping[l] for l in llms],
#                                 columns=[model_mapping[l] for l in llms])
#
# func_overlap_df.to_csv('../results/rq3_function_jaccard_matrix_intersection.csv')
# class_overlap_df.to_csv('../results/rq3_class_jaccard_matrix_intersection.csv')
# print('✓ Saved: ../results/rq3_function_jaccard_matrix_intersection.csv')
# print('✓ Saved: ../results/rq3_class_jaccard_matrix_intersection.csv')
#
# # Granularity overlap
# granularity_df.to_csv('../results/rq3_granularity_overlap_intersection.csv', index=False)
# print('✓ Saved: ../results/rq3_granularity_overlap_intersection.csv')
#
# # Feature frequency
# freq_df.to_csv('../results/rq3_feature_frequency_intersection.csv', index=False)
# print('✓ Saved: ../results/rq3_feature_frequency_intersection.csv')
#
# # Summary statistics
# summary_stats = {
#     'Metric': [
#         'Avg Function-level Jaccard (cross-model)',
#         'Avg Class-level Jaccard (cross-model)',
#         'Avg Cross-granularity Jaccard (within-model)',
#         'Universal Features Count',
#         'Highly Common Features Count',
#         'Function-level Perfect Overlap'
#     ],
#     'Value': [
#         1.0 if all_identical else np.mean([func_overlap_numeric[i, j]
#                                            for i in range(4) for j in range(i + 1, 4)]),
#         np.mean(class_overlap_values),
#         granularity_df['Jaccard'].mean(),
#         len(universal_features),
#         len(highly_common_features),
#         'Yes' if all_identical else 'No'
#     ]
# }
#
# summary_df = pd.DataFrame(summary_stats)
# summary_df.to_csv('../results/rq3_summary_statistics_intersection.csv', index=False)
# print('✓ Saved: ../results/rq3_summary_statistics_intersection.csv')
#
# print('\n' + '=' * 80)
# print('RQ3 ANALYSIS COMPLETE!')
# print('=' * 80)
# print('\nKey Findings:')
# print(f'1. Function-level feature convergence: {"PERFECT" if all_identical else "PARTIAL"}')
# print(f'2. Class-level average overlap: {np.mean(class_overlap_values):.3f}')
# print(f'3. Cross-granularity overlap: {granularity_df["Jaccard"].mean():.3f}')
# print(f'4. Granularity effect vs model effect: {avg_cross_model_class / avg_cross_granularity:.1f}x stronger')
# print(f'5. Universal features: {len(universal_features)}')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11

# ============================================================
# FEATURE NAME MAPPING
# ============================================================

FEATURE_NAME_MAPPING = {
    # Function-level features
    'MaxNesting': 'Maximum Nesting Depth',
    'CountLineBlank': 'Blank Lines',
    'CountStmtDecl': 'Declarative Statements',
    'CountPathLog': 'Logarithmic Paths',
    'RatioCommentToCode': 'Comment-to-Code Ratio',
    'Essential': 'Essential Complexity',
    'CountLineComment': 'Comment Lines',
    'CountLineCodeDecl': 'Declarative Code Lines',
    'CountLine': 'Lines',
    'CountLineCode': 'Code Lines',
    'CountLineCodeExe': 'Executable Code Lines',
    'CountStmt': 'Statements',
    'CountStmtExe': 'Executable Statements',
    'Cyclomatic': 'Cyclomatic Complexity',
    'CyclomaticModified': 'Modified Cyclomatic Complexity',
    'CyclomaticStrict': 'Strict Cyclomatic Complexity',
    'Essential': 'Essential Complexity',
    'CountPath': 'Paths',

    # Class-level features
    'CountClassBase': 'Base Classes',
    'AvgCountLineCode': 'Average Code Lines',
    'CountDeclInstanceMethod': 'Instance Methods',
    'CountDeclInstanceVariable': 'Instance Variables',
    'CountClassCoupledModified': 'Modified Coupled Classes',
    'CountClassDerived': 'Derived Classes',
    'AvgEssential': 'Average Essential Complexity',
    'CountClassCoupled': 'Coupled Classes',
    'AvgCountLineComment': 'Average Comment Lines',
    'AvgCountLineBlank': 'Average Blank Lines',
    'MaxInheritanceTree': 'Maximum Inheritance Tree',
    'CountDeclMethod': 'Methods',
    'CountDeclMethodAll': 'All Methods',
    'AvgCyclomatic': 'Average Cyclomatic Complexity',
    'AvgCyclomaticModified': 'Average Modified Cyclomatic Complexity',
    'AvgCyclomaticStrict': 'Average Strict Cyclomatic Complexity',
    'MaxCyclomatic': 'Maximum Cyclomatic Complexity',
    'MaxCyclomaticModified': 'Maximum Modified Cyclomatic Complexity',
    'MaxCyclomaticStrict': 'Maximum Strict Cyclomatic Complexity',
    'MaxEssential': 'Maximum Essential Complexity',
    'SumCyclomatic': 'Sum Cyclomatic Complexity',
    'SumCyclomaticModified': 'Sum Modified Cyclomatic Complexity',
    'SumCyclomaticStrict': 'Sum Strict Cyclomatic Complexity',
    'SumEssential': 'Sum Essential Complexity',
}


def get_readable_name(feature):
    """Convert technical feature name to human-readable format."""
    return FEATURE_NAME_MAPPING.get(feature, feature)


print('=' * 80)
print('RQ3: FEATURE OVERLAP AND GENERALIZATION PATTERN ANALYSIS')
print('USING INTERSECTION DATA')
print('=' * 80)

# ============================================================
# Load AutoSpearman Selected Features
# ============================================================

print('\nLoading AutoSpearman selected features from intersection data...')

# Model mapping
model_mapping = {
    'claude-3-haiku': 'Claude 3 Haiku',
    'claude-4-5-haiku': 'Claude 4.5 Haiku',
    'gpt-3-5': 'GPT-3.5',
    'gpt-oss': 'GPT-OSS'
}

# Load selected features for each configuration
selected_features = {}

for llm in ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
    for granularity in ['Function', 'Class']:
        config_key = f'{llm}_{granularity}'

        # Try to load from test data (features are the columns minus 'label')
        try:
            test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
            features = [col for col in test_data.columns if col != 'label']
            selected_features[config_key] = set(features)
            print(f'✓ Loaded {len(features)} features for {model_mapping[llm]} {granularity}')
        except FileNotFoundError:
            print(f'✗ Could not find test data for {llm} {granularity}')
            selected_features[config_key] = set()


# ============================================================
# Jaccard Similarity Analysis
# ============================================================

def jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity coefficient."""
    if len(set1) == 0 and len(set2) == 0:
        return 1.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0


def interpret_jaccard(j):
    """Interpret Jaccard similarity."""
    if j >= 0.8:
        return "Very High"
    elif j >= 0.6:
        return "High"
    elif j >= 0.4:
        return "Moderate"
    elif j >= 0.2:
        return "Low"
    else:
        return "Negligible"


print('\n' + '=' * 80)
print('CROSS-MODEL FEATURE OVERLAP (SAME GRANULARITY)')
print('=' * 80)

# Function-level overlap
print('\n--- FUNCTION-LEVEL OVERLAP ---\n')

llms = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
function_overlap_matrix = pd.DataFrame(index=[model_mapping[l] for l in llms],
                                       columns=[model_mapping[l] for l in llms])

for i, llm1 in enumerate(llms):
    for j, llm2 in enumerate(llms):
        if i == j:
            # Diagonal: show feature count
            count = len(selected_features[f'{llm1}_Function'])
            function_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"({count})"
        else:
            # Off-diagonal: Jaccard similarity
            jaccard = jaccard_similarity(
                selected_features[f'{llm1}_Function'],
                selected_features[f'{llm2}_Function']
            )
            function_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"{jaccard:.3f}"

print('Function-level Jaccard Similarity Matrix:')
print(function_overlap_matrix)

# Check if all function-level features are identical
function_features_list = [selected_features[f'{llm}_Function'] for llm in llms]
all_identical = all(f == function_features_list[0] for f in function_features_list)

if all_identical:
    print('\n⭐ CRITICAL FINDING: All function-level models use IDENTICAL feature sets!')
    print(f'   Universal feature set size: {len(function_features_list[0])}')
    print(f'   Features: {sorted([get_readable_name(f) for f in function_features_list[0]])}')
else:
    print('\n   Function-level features vary by model')

# Class-level overlap
print('\n--- CLASS-LEVEL OVERLAP ---\n')

class_overlap_matrix = pd.DataFrame(index=[model_mapping[l] for l in llms],
                                    columns=[model_mapping[l] for l in llms])

class_overlap_values = []
for i, llm1 in enumerate(llms):
    for j, llm2 in enumerate(llms):
        if i == j:
            # Diagonal: show feature count
            count = len(selected_features[f'{llm1}_Class'])
            class_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"({count})"
        else:
            # Off-diagonal: Jaccard similarity
            jaccard = jaccard_similarity(
                selected_features[f'{llm1}_Class'],
                selected_features[f'{llm2}_Class']
            )
            class_overlap_matrix.loc[model_mapping[llm1], model_mapping[llm2]] = f"{jaccard:.3f}"
            if i < j:  # Only count each pair once
                class_overlap_values.append(jaccard)

print('Class-level Jaccard Similarity Matrix:')
print(class_overlap_matrix)

print(f'\nClass-level Statistics:')
print(f'  Average Jaccard: {np.mean(class_overlap_values):.3f}')
print(f'  Range: [{np.min(class_overlap_values):.3f}, {np.max(class_overlap_values):.3f}]')
print(f'  Interpretation: {interpret_jaccard(np.mean(class_overlap_values))}')

# ============================================================
# CROSS-GRANULARITY OVERLAP (WITHIN MODEL)
# ============================================================

print('\n' + '=' * 80)
print('CROSS-GRANULARITY FEATURE OVERLAP (WITHIN MODEL)')
print('=' * 80 + '\n')

granularity_overlap = []
for llm in llms:
    func_features = selected_features[f'{llm}_Function']
    class_features = selected_features[f'{llm}_Class']

    jaccard = jaccard_similarity(func_features, class_features)
    overlap = func_features.intersection(class_features)

    granularity_overlap.append({
        'Model': model_mapping[llm],
        'Function_Features': len(func_features),
        'Class_Features': len(class_features),
        'Overlap_Count': len(overlap),
        'Jaccard': jaccard,
        'Interpretation': interpret_jaccard(jaccard)
    })

    print(f'{model_mapping[llm]:20s}:')
    print(f'  Function features: {len(func_features)}')
    print(f'  Class features:    {len(class_features)}')
    print(f'  Overlap:           {len(overlap)} features')
    print(f'  Jaccard:           {jaccard:.3f} ({interpret_jaccard(jaccard)})')
    print(f'  Shared features:   {sorted([get_readable_name(f) for f in overlap]) if overlap else "None"}')
    print()

granularity_df = pd.DataFrame(granularity_overlap)

print('Summary Statistics:')
print(f'  Average cross-granularity Jaccard: {granularity_df["Jaccard"].mean():.3f}')
print(f'  Range: [{granularity_df["Jaccard"].min():.3f}, {granularity_df["Jaccard"].max():.3f}]')

# Compare to cross-model overlap
avg_cross_model_class = np.mean(class_overlap_values)
avg_cross_granularity = granularity_df["Jaccard"].mean()

print(f'\n⭐ KEY COMPARISON:')
print(f'  Cross-model overlap (same granularity): {avg_cross_model_class:.3f}')
print(f'  Cross-granularity overlap (same model): {avg_cross_granularity:.3f}')
print(f'  Ratio: {avg_cross_model_class / avg_cross_granularity:.1f}x')
print(
    f'\n  → Granularity affects features {avg_cross_model_class / avg_cross_granularity:.1f}x MORE than model choice!')

# ============================================================
# UNIVERSAL FEATURES ANALYSIS
# ============================================================

print('\n' + '=' * 80)
print('UNIVERSAL FEATURES ACROSS ALL CONFIGURATIONS')
print('=' * 80 + '\n')

# Count feature frequency across all 8 configurations
feature_frequency = {}
all_features = set()

for config_key, features in selected_features.items():
    all_features.update(features)
    for feature in features:
        feature_frequency[feature] = feature_frequency.get(feature, 0) + 1

# Categorize features
universal_features = [f for f, count in feature_frequency.items() if count == 8]
highly_common_features = [f for f, count in feature_frequency.items() if 6 <= count < 8]
common_features = [f for f, count in feature_frequency.items() if 4 <= count < 6]
model_specific_features = [f for f, count in feature_frequency.items() if count < 4]

print(f'Total unique features across all configurations: {len(all_features)}')
print(f'\nFeature Categories:')
print(f'  Universal (8/8 configs):      {len(universal_features)} features')
print(f'  Highly Common (6-7/8):        {len(highly_common_features)} features')
print(f'  Common (4-5/8):               {len(common_features)} features')
print(f'  Model/Granularity-Specific:   {len(model_specific_features)} features')

print(f'\n⭐ UNIVERSAL FEATURES (appear in all 8 configurations):')
if universal_features:
    for feature in sorted(universal_features):
        print(f'  - {get_readable_name(feature)}')
else:
    print('  (None)')

print(f'\nHIGHLY COMMON FEATURES (6-7/8 configurations):')
for feature in sorted(highly_common_features):
    count = feature_frequency[feature]
    print(f'  - {get_readable_name(feature):35s} ({count}/8)')

# Detailed frequency table with readable names
freq_df = pd.DataFrame([
    {'Feature': get_readable_name(f), 'Technical_Name': f, 'Frequency': count, 'Percentage': f'{count / 8 * 100:.0f}%'}
    for f, count in sorted(feature_frequency.items(), key=lambda x: (-x[1], x[0]))
])

# ============================================================
# VISUALIZATION 1: Heatmap of Feature Overlap
# ============================================================

print('\n' + '=' * 80)
print('GENERATING VISUALIZATIONS')
print('=' * 80 + '\n')

os.makedirs('../plots_for_paper', exist_ok=True)
os.makedirs('../results', exist_ok=True)

# Create numerical matrices for heatmap
func_overlap_numeric = np.zeros((4, 4))
class_overlap_numeric = np.zeros((4, 4))

for i, llm1 in enumerate(llms):
    for j, llm2 in enumerate(llms):
        if i == j:
            func_overlap_numeric[i, j] = 1.0
            class_overlap_numeric[i, j] = 1.0
        else:
            func_overlap_numeric[i, j] = jaccard_similarity(
                selected_features[f'{llm1}_Function'],
                selected_features[f'{llm2}_Function']
            )
            class_overlap_numeric[i, j] = jaccard_similarity(
                selected_features[f'{llm1}_Class'],
                selected_features[f'{llm2}_Class']
            )

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Function-level heatmap
sns.heatmap(func_overlap_numeric, annot=True, fmt='.3f', cmap='YlOrRd',
            xticklabels=[model_mapping[l] for l in llms],
            yticklabels=[model_mapping[l] for l in llms],
            vmin=0, vmax=1, cbar_kws={'label': 'Jaccard Similarity'},
            ax=axes[0], linewidths=0.5, linecolor='gray')
axes[0].set_title('Function-Level Feature Overlap', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Model', fontweight='bold')
axes[0].set_ylabel('Model', fontweight='bold')

# Class-level heatmap
sns.heatmap(class_overlap_numeric, annot=True, fmt='.3f', cmap='YlOrRd',
            xticklabels=[model_mapping[l] for l in llms],
            yticklabels=[model_mapping[l] for l in llms],
            vmin=0, vmax=1, cbar_kws={'label': 'Jaccard Similarity'},
            ax=axes[1], linewidths=0.5, linecolor='gray')
axes[1].set_title('Class-Level Feature Overlap', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Model', fontweight='bold')
axes[1].set_ylabel('Model', fontweight='bold')

plt.tight_layout()
plt.savefig('../plots_for_paper/rq3_feature_overlap_heatmaps_intersection.pdf', dpi=300, bbox_inches='tight')
print('✓ Saved: ../plots_for_paper/rq3_feature_overlap_heatmaps_intersection.pdf')

# ============================================================
# VISUALIZATION 2: Feature Frequency Bar Chart (HUMAN-READABLE)
# ============================================================

fig, ax = plt.subplots(figsize=(12, 8))

# Get top 20 features by frequency
top_features = freq_df.head(20)

colors = ['#d62728' if row['Frequency'] == 8 else  # Universal (red)
          '#ff7f0e' if row['Frequency'] >= 6 else  # Highly common (orange)
          '#2ca02c' if row['Frequency'] >= 4 else  # Common (green)
          '#1f77b4'  # Model-specific (blue)
          for _, row in top_features.iterrows()]

bars = ax.barh(range(len(top_features)), top_features['Frequency'], color=colors)
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'])  # Now uses human-readable names
ax.set_xlabel('Number of Configurations (out of 8)', fontweight='bold', fontsize=12)
ax.set_ylabel('Feature', fontweight='bold', fontsize=12)
ax.set_title('Top 20 Features by Frequency Across Configurations',
             fontsize=14, fontweight='bold')
ax.set_xlim(0, 8.5)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, freq) in enumerate(zip(bars, top_features['Frequency'])):
    ax.text(freq + 0.1, i, f'{freq}/8', va='center', fontweight='bold')

# Legend
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor='#d62728', label='Universal (8/8)'),
    Patch(facecolor='#ff7f0e', label='Highly Common (6-7/8)'),
    Patch(facecolor='#2ca02c', label='Common (4-5/8)'),
    Patch(facecolor='#1f77b4', label='Model-Specific (<4/8)')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('../plots_for_paper/rq3_feature_frequency_intersection.pdf', dpi=300, bbox_inches='tight')
print('✓ Saved: ../plots_for_paper/rq3_feature_frequency_intersection.pdf')

# ============================================================
# SAVE RESULTS TO CSV
# ============================================================

# Feature overlap matrices
func_overlap_df = pd.DataFrame(func_overlap_numeric,
                               index=[model_mapping[l] for l in llms],
                               columns=[model_mapping[l] for l in llms])
class_overlap_df = pd.DataFrame(class_overlap_numeric,
                                index=[model_mapping[l] for l in llms],
                                columns=[model_mapping[l] for l in llms])

func_overlap_df.to_csv('../results/rq3_function_jaccard_matrix_intersection.csv')
class_overlap_df.to_csv('../results/rq3_class_jaccard_matrix_intersection.csv')
print('✓ Saved: ../results/rq3_function_jaccard_matrix_intersection.csv')
print('✓ Saved: ../results/rq3_class_jaccard_matrix_intersection.csv')

# Granularity overlap
granularity_df.to_csv('../results/rq3_granularity_overlap_intersection.csv', index=False)
print('✓ Saved: ../results/rq3_granularity_overlap_intersection.csv')

# Feature frequency (with both readable and technical names)
freq_df.to_csv('../results/rq3_feature_frequency_intersection.csv', index=False)
print('✓ Saved: ../results/rq3_feature_frequency_intersection.csv')

# Summary statistics
summary_stats = {
    'Metric': [
        'Avg Function-level Jaccard (cross-model)',
        'Avg Class-level Jaccard (cross-model)',
        'Avg Cross-granularity Jaccard (within-model)',
        'Universal Features Count',
        'Highly Common Features Count',
        'Function-level Perfect Overlap'
    ],
    'Value': [
        1.0 if all_identical else np.mean([func_overlap_numeric[i, j]
                                           for i in range(4) for j in range(i + 1, 4)]),
        np.mean(class_overlap_values),
        granularity_df['Jaccard'].mean(),
        len(universal_features),
        len(highly_common_features),
        'Yes' if all_identical else 'No'
    ]
}

summary_df = pd.DataFrame(summary_stats)
summary_df.to_csv('../results/rq3_summary_statistics_intersection.csv', index=False)
print('✓ Saved: ../results/rq3_summary_statistics_intersection.csv')

print('\n' + '=' * 80)
print('RQ3 ANALYSIS COMPLETE!')
print('=' * 80)
print('\nKey Findings:')
print(f'1. Function-level feature convergence: {"PERFECT" if all_identical else "PARTIAL"}')
print(f'2. Class-level average overlap: {np.mean(class_overlap_values):.3f}')
print(f'3. Cross-granularity overlap: {granularity_df["Jaccard"].mean():.3f}')
print(f'4. Granularity effect vs model effect: {avg_cross_model_class / avg_cross_granularity:.1f}x stronger')
print(f'5. Universal features: {len(universal_features)}')
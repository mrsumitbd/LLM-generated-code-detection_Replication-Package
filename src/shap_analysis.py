# """
# Extract SHAP values from trained CatBoost models and generate comprehensive analysis.
# USING INTERSECTION DATA
#
# This script:
# 1. Loads all 8 trained models (4 LLMs × 2 granularities) trained on intersection data
# 2. Computes SHAP values on test sets
# 3. Extracts mean absolute SHAP importance for each feature
# 4. Generates CSV files with actual SHAP data
# 5. Creates statistical analysis
# 6. Generates visualizations
#
# Usage:
#     python extract_shap_values_intersection.py
# """
#
# import pandas as pd
# import numpy as np
# import pickle
# import shap
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.colors import LinearSegmentedColormap
# from scipy.stats import mannwhitneyu, permutation_test
# import warnings
# import os
#
# warnings.filterwarnings('ignore')
#
# # Configuration
# MODELS = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
# GRANULARITIES = ['Function', 'Class']
# MODEL_NAMES = {
#     'claude-3-haiku': 'Claude 3 Haiku',
#     'claude-4-5-haiku': 'Claude 4.5 Haiku',
#     'gpt-3-5': 'GPT-3.5',
#     'gpt-oss': 'GPT-OSS'
# }
#
# # Output directories
# os.makedirs('../results', exist_ok=True)
# os.makedirs('../plots_for_paper', exist_ok=True)
#
# print('='*80)
# print('EXTRACTING SHAP VALUES FROM TRAINED MODELS (INTERSECTION DATA)')
# print('='*80)
#
# # ============================================================
# # Step 1: Extract SHAP values from all models
# # ============================================================
#
# all_shap_data = {}
# shap_summary = []
#
# for llm in MODELS:
#     for granularity in GRANULARITIES:
#         config_key = f'{llm}_{granularity}'
#
#         print(f'\nProcessing {MODEL_NAMES[llm]} {granularity}-level...')
#
#         # Load model (intersection version)
#         model_path = f'../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl'
#         with open(model_path, 'rb') as f:
#             model = pickle.load(f)
#
#         # Load test data (intersection version)
#         test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
#         X_test = test_data.drop(columns=['label'])
#         y_test = test_data['label']
#
#         # Compute SHAP values
#         explainer = shap.TreeExplainer(model)
#         shap_values = explainer.shap_values(X_test)
#
#         # For binary classification, get positive class (LLM) SHAP values
#         if isinstance(shap_values, list):
#             shap_values = shap_values[1]
#
#         # Calculate mean absolute SHAP importance
#         feature_importance = np.abs(shap_values).mean(axis=0)
#         feature_names = X_test.columns.tolist()
#
#         # Store for this configuration
#         importance_dict = dict(zip(feature_names, feature_importance))
#         all_shap_data[config_key] = importance_dict
#
#         # Create sorted dataframe
#         importance_df = pd.DataFrame({
#             'Feature': feature_names,
#             'SHAP_Importance': feature_importance
#         }).sort_values('SHAP_Importance', ascending=False)
#
#         # Add to summary
#         for rank, (idx, row) in enumerate(importance_df.iterrows(), 1):
#             shap_summary.append({
#                 'Model': llm,
#                 'Model_Name': MODEL_NAMES[llm],
#                 'Granularity': granularity,
#                 'Config': config_key,
#                 'Feature': row['Feature'],
#                 'SHAP_Importance': row['SHAP_Importance'],
#                 'Rank': rank
#             })
#
#         print(f'  ✓ Extracted {len(feature_names)} features')
#         print(f'  Top 3: {", ".join(importance_df.head(3)["Feature"].tolist())}')
#
# print('\n✓ SHAP extraction complete for all 8 configurations')
#
# # Save comprehensive SHAP data
# shap_df = pd.DataFrame(shap_summary)
# shap_df.to_csv('../results/shap_values_all_configs_intersection.csv', index=False)
# print(f'\n✓ Saved: ../results/shap_values_all_configs_intersection.csv')
#
# # ============================================================
# # Step 2: Generate Beeswarm Plots for All Configurations
# # ============================================================
#
# print('\n' + '='*80)
# print('GENERATING SHAP BEESWARM PLOTS')
# print('='*80)
#
# # Store SHAP values for later analysis
# all_shap_values = {}
# all_X_test = {}
#
# for llm in MODELS:
#     for granularity in GRANULARITIES:
#         config_key = f'{llm}_{granularity}'
#
#         print(f'\nGenerating beeswarm plot for {MODEL_NAMES[llm]} {granularity}-level...')
#
#         # Load model and data again
#         model_path = f'../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl'
#         with open(model_path, 'rb') as f:
#             model = pickle.load(f)
#
#         test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
#         X_test = test_data.drop(columns=['label'])
#
#         # Compute SHAP values
#         explainer = shap.TreeExplainer(model)
#         shap_values = explainer.shap_values(X_test)
#
#         # For binary classification, get positive class (LLM)
#         if isinstance(shap_values, list):
#             shap_values = shap_values[1]
#
#         # Store for later use
#         all_shap_values[config_key] = shap_values
#         all_X_test[config_key] = X_test
#
#         # Create beeswarm plot
#         fig, ax = plt.subplots(figsize=(12, 8))
#         shap.summary_plot(shap_values, X_test, show=False)  # Show ALL features
#
#         # Add vertical line at 0
#         ax.axvline(x=0, color='black', linestyle='-', linewidth=2, alpha=0.8, zorder=0)
#
#         # Get current axis limits
#         xlim = ax.get_xlim()
#         ylim = ax.get_ylim()
#
#         # Add colored backgrounds
#         ax.axvspan(xlim[0], 0, alpha=0.1, color='blue', zorder=0)
#         ax.axvspan(0, xlim[1], alpha=0.1, color='red', zorder=0)
#
#         # Add text labels
#         ax.text(xlim[0] * 0.5, ylim[1] * 0.98, '← Human',
#                 fontsize=13, ha='center', va='top',
#                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7), weight='bold')
#         ax.text(xlim[1] * 0.5, ylim[1] * 0.98, 'LLM →',
#                 fontsize=13, ha='center', va='top',
#                 bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7), weight='bold')
#
#         ax.set_xlabel('SHAP Value (impact on model output)', fontsize=12, fontweight='bold')
#         ax.set_title(f'{MODEL_NAMES[llm]} {granularity}-level: Feature Importance',
#                      fontsize=14, pad=20, weight='bold')
#
#         plt.tight_layout()
#
#         # Save plot
#         output_filename = f'../plots_for_paper/{llm}_{granularity}_catboost_shap_beeswarm_intersection.pdf'
#         plt.savefig(output_filename, dpi=300, bbox_inches='tight')
#         plt.close()
#
#         print(f'  ✓ Saved: {output_filename}')
#
# print('\n✓ All beeswarm plots generated successfully')
#
# # ============================================================
# # Step 3: Generate Feature Importance Summary
# # ============================================================
#
# print('\n' + '='*80)
# print('GENERATING FEATURE IMPORTANCE SUMMARY')
# print('='*80)
#
# # Get all unique features
# all_features = set()
# for config_data in all_shap_data.values():
#     all_features.update(config_data.keys())
#
# # Create frequency and importance summary
# feature_summary = []
# for feature in all_features:
#     configs_present = []
#     importances = []
#     top3_count = 0
#
#     for config_key, importance_dict in all_shap_data.items():
#         if feature in importance_dict:
#             configs_present.append(config_key)
#             importances.append(importance_dict[feature])
#
#             # Check if in top 3 for this config
#             sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
#             if feature in [f[0] for f in sorted_features[:3]]:
#                 top3_count += 1
#
#     if importances:
#         feature_summary.append({
#             'Feature': feature,
#             'Frequency': len(configs_present),
#             'Percentage': f'{len(configs_present)/8*100:.0f}%',
#             'Avg_Importance': np.mean(importances),
#             'Max_Importance': np.max(importances),
#             'Top3_Count': top3_count,
#             'Configs': ', '.join(configs_present)
#         })
#
# feature_summary_df = pd.DataFrame(feature_summary).sort_values('Avg_Importance', ascending=False)
# feature_summary_df.to_csv('../results/feature_importance_summary_intersection.csv', index=False)
# print('✓ Saved: ../results/feature_importance_summary_intersection.csv')
#
# print('\nTop 10 Features by Average Importance:')
# print(feature_summary_df[['Feature', 'Frequency', 'Avg_Importance', 'Top3_Count']].head(10).to_string(index=False))
#
# # ============================================================
# # Step 4: Analyze RatioCommentToCode across configs
# # ============================================================
#
# print('\n' + '='*80)
# print('ANALYZING RATIOCOMMENTTOCODE IMPORTANCE')
# print('='*80)
#
# ratio_importance = {}
# for config_key, importance_dict in all_shap_data.items():
#     if 'RatioCommentToCode' in importance_dict:
#         ratio_importance[config_key] = importance_dict['RatioCommentToCode']
#
# if ratio_importance:
#     ratio_df = pd.DataFrame(list(ratio_importance.items()), columns=['Config', 'SHAP_Importance'])
#     ratio_df['Model'] = ratio_df['Config'].apply(lambda x: x.rsplit('_', 1)[0])
#     ratio_df['Granularity'] = ratio_df['Config'].apply(lambda x: x.rsplit('_', 1)[1])
#
#     print('\nRatioCommentToCode SHAP Importance by Config:')
#     for _, row in ratio_df.iterrows():
#         print(f'  {row["Config"]:30s}: {row["SHAP_Importance"]:.4f}')
#
#     # Function vs Class comparison
#     func_values = ratio_df[ratio_df['Granularity'] == 'Function']['SHAP_Importance'].values
#     class_values = ratio_df[ratio_df['Granularity'] == 'Class']['SHAP_Importance'].values
#
#     if len(func_values) > 0 and len(class_values) > 0:
#         print(f'\nFunction-level mean: {func_values.mean():.4f}')
#         print(f'Class-level mean:    {class_values.mean():.4f}')
#         print(f'Ratio (Func/Class):  {func_values.mean() / class_values.mean():.2f}x')
#
#         # Permutation test
#         def mean_diff(x, y, axis=-1):
#             return np.mean(x, axis=axis) - np.mean(y, axis=axis)
#
#         if len(func_values) >= 2 and len(class_values) >= 2:
#             res = permutation_test((func_values, class_values), mean_diff,
#                                   n_resamples=10000, alternative='two-sided')
#             print(f'Permutation test p-value: {res.pvalue:.4f}')
#             print(f'Significant: {"Yes" if res.pvalue < 0.05 else "No"}')
#         else:
#             print('Not enough data for permutation test')
#             res = None
#     else:
#         print('RatioCommentToCode not found in enough configs for comparison')
#         res = None
#
#     ratio_df.to_csv('../results/ratiocommenttocode_analysis_intersection.csv', index=False)
#     print('\n✓ Saved: ../results/ratiocommenttocode_analysis_intersection.csv')
# else:
#     print('\nRatioCommentToCode not found in any configuration')
#     res = None
#
# # ============================================================
# # Step 5: Model-Specific Average Importance
# # ============================================================
#
# print('\n' + '='*80)
# print('MODEL-SPECIFIC AVERAGE IMPORTANCE')
# print('='*80)
#
# model_stats = []
# for llm in MODELS:
#     func_config = f'{llm}_Function'
#     class_config = f'{llm}_Class'
#
#     func_importances = list(all_shap_data[func_config].values())
#     class_importances = list(all_shap_data[class_config].values())
#
#     model_stats.append({
#         'Model': llm,
#         'Model_Name': MODEL_NAMES[llm],
#         'Function_Mean': np.mean(func_importances),
#         'Function_Max': np.max(func_importances),
#         'Class_Mean': np.mean(class_importances),
#         'Class_Max': np.max(class_importances),
#         'Overall_Mean': np.mean(func_importances + class_importances)
#     })
#
# model_stats_df = pd.DataFrame(model_stats).sort_values('Overall_Mean', ascending=False)
# model_stats_df.to_csv('../results/model_importance_statistics_intersection.csv', index=False)
# print('✓ Saved: ../results/model_importance_statistics_intersection.csv')
#
# print('\nModel Importance Summary:')
# print(model_stats_df[['Model_Name', 'Function_Mean', 'Class_Mean', 'Overall_Mean']].to_string(index=False))
#
# # ============================================================
# # Step 6: Top Feature Rankings
# # ============================================================
#
# print('\n' + '='*80)
# print('TOP FEATURE RANKINGS BY CONFIGURATION')
# print('='*80)
#
# top_features_per_config = []
# for config_key, importance_dict in all_shap_data.items():
#     sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
#
#     llm, granularity = config_key.rsplit('_', 1)
#
#     for rank, (feature, importance) in enumerate(sorted_features, 1):
#         top_features_per_config.append({
#             'Config': config_key,
#             'Model': llm,
#             'Model_Name': MODEL_NAMES[llm],
#             'Granularity': granularity,
#             'Rank': rank,
#             'Feature': feature,
#             'SHAP_Importance': importance,
#             'Is_Top3': 'Yes' if rank <= 3 else 'No'
#         })
#
# top_features_df = pd.DataFrame(top_features_per_config)
# top_features_df.to_csv('../results/feature_rankings_all_configs_intersection.csv', index=False)
# print('✓ Saved: ../results/feature_rankings_all_configs_intersection.csv')
#
# # Show #1 feature for each config
# print('\n#1 Feature by Configuration:')
# rank1_df = top_features_df[top_features_df['Rank'] == 1]
# for _, row in rank1_df.iterrows():
#     print(f'  {row["Config"]:30s}: {row["Feature"]:30s} ({row["SHAP_Importance"]:.4f})')
#
# # ============================================================
# # Step 7: Generate Heatmap with ACTUAL Data
# # ============================================================
#
# print('\n' + '='*80)
# print('GENERATING VISUALIZATIONS')
# print('='*80)
#
# # Create heatmap matrix
# heatmap_data = {}
# for config_key, importance_dict in all_shap_data.items():
#     llm, granularity = config_key.rsplit('_', 1)
#     for feature, importance in importance_dict.items():
#         if feature not in heatmap_data:
#             heatmap_data[feature] = {}
#         col_name = f'{MODEL_NAMES[llm]}\n{granularity}'
#         heatmap_data[feature][col_name] = importance
#
# heatmap_df = pd.DataFrame(heatmap_data).T.fillna(0)
#
# # Reorder columns
# column_order = []
# for llm in MODELS:
#     for gran in GRANULARITIES:
#         col_name = f'{MODEL_NAMES[llm]}\n{gran}'
#         if col_name in heatmap_df.columns:
#             column_order.append(col_name)
#
# heatmap_df = heatmap_df[column_order]
#
# # Sort by max importance
# heatmap_df['max_importance'] = heatmap_df.max(axis=1)
# heatmap_df = heatmap_df.sort_values('max_importance', ascending=False)
# heatmap_df = heatmap_df.drop('max_importance', axis=1)
#
# # Create heatmap
# fig, ax = plt.subplots(figsize=(14, 10))
# cmap = LinearSegmentedColormap.from_list('custom',
#                                          ['white', '#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'])
#
# sns.heatmap(heatmap_df, annot=True, fmt='.3f', cmap=cmap,
#             cbar_kws={'label': 'SHAP Importance'},
#             linewidths=0.5, linecolor='gray', ax=ax,
#             vmin=0, vmax=heatmap_df.max().max())
#
# ax.set_title('Feature Importance Across Models and Granularities\n(SHAP Values - Intersection Data)',
#              fontsize=16, fontweight='bold', pad=20)
# ax.set_xlabel('Model × Granularity', fontsize=13, fontweight='bold')
# ax.set_ylabel('Feature', fontsize=13, fontweight='bold')
#
# plt.xticks(rotation=45, ha='right')
# plt.yticks(rotation=0)
#
# # Add vertical lines
# for i in [2, 4, 6]:
#     ax.axvline(x=i, color='black', linewidth=2)
#
# plt.tight_layout()
# plt.savefig('../plots_for_paper/feature_importance_heatmap_intersection.pdf', dpi=300, bbox_inches='tight')
# print('✓ Saved: ../plots_for_paper/feature_importance_heatmap_intersection.pdf')
#
# # Top 10 version
# top10_df = heatmap_df.head(10)
# fig, ax = plt.subplots(figsize=(12, 6))
#
# sns.heatmap(top10_df, annot=True, fmt='.3f', cmap=cmap,
#             cbar_kws={'label': 'SHAP Importance'},
#             linewidths=0.5, linecolor='gray', ax=ax,
#             vmin=0, vmax=heatmap_df.max().max())
#
# ax.set_title('Top 10 Features: Importance Across Models and Granularities',
#              fontsize=15, fontweight='bold', pad=15)
# ax.set_xlabel('Model × Granularity', fontsize=12, fontweight='bold')
# ax.set_ylabel('Feature', fontsize=12, fontweight='bold')
#
# plt.xticks(rotation=45, ha='right')
# plt.yticks(rotation=0)
#
# for i in [2, 4, 6]:
#     ax.axvline(x=i, color='black', linewidth=2)
#
# plt.tight_layout()
# plt.savefig('../plots_for_paper/feature_importance_heatmap_top10_intersection.pdf', dpi=300, bbox_inches='tight')
# print('✓ Saved: ../plots_for_paper/feature_importance_heatmap_top10_intersection.pdf')
#
# # ============================================================
# # Step 8: Statistical Tests
# # ============================================================
#
# print('\n' + '='*80)
# print('STATISTICAL TESTS')
# print('='*80)
#
# statistical_tests = []
#
# # Test 1: Overall distribution comparison (Function vs Class)
# all_func_importance = []
# all_class_importance = []
#
# for config_key, importance_dict in all_shap_data.items():
#     granularity = config_key.rsplit('_', 1)[1]
#     if granularity == 'Function':
#         all_func_importance.extend(importance_dict.values())
#     else:
#         all_class_importance.extend(importance_dict.values())
#
# u_stat, p_val = mannwhitneyu(all_func_importance, all_class_importance, alternative='two-sided')
#
# def cohens_d(x, y):
#     nx, ny = len(x), len(y)
#     dof = nx + ny - 2
#     return (np.mean(x) - np.mean(y)) / np.sqrt(
#         ((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / dof)
#
# effect_size = cohens_d(all_func_importance, all_class_importance)
#
# statistical_tests.append({
#     'Test': 'Mann-Whitney U',
#     'Comparison': 'Function vs Class (All Features)',
#     'Statistic': u_stat,
#     'P-value': p_val,
#     'Effect_Size': effect_size,
#     'Interpretation': 'Negligible' if abs(effect_size) < 0.2 else 'Small' if abs(effect_size) < 0.5 else 'Medium' if abs(effect_size) < 0.8 else 'Large'
# })
#
# print(f'\nMann-Whitney U Test (Function vs Class):')
# print(f'  U-statistic: {u_stat:.2f}')
# print(f'  p-value: {p_val:.4f}')
# print(f'  Cohen\'s d: {effect_size:.4f}')
#
# # Test 2: RatioCommentToCode Function vs Class (if available)
# if res is not None and ratio_importance:
#     statistical_tests.append({
#         'Test': 'Permutation Test',
#         'Comparison': 'RatioCommentToCode: Function vs Class',
#         'Statistic': func_values.mean() - class_values.mean(),
#         'P-value': res.pvalue,
#         'Effect_Size': func_values.mean() / class_values.mean(),
#         'Interpretation': f'{func_values.mean() / class_values.mean():.1f}x higher at function-level'
#     })
#
# stats_df = pd.DataFrame(statistical_tests)
# stats_df.to_csv('../results/statistical_tests_intersection.csv', index=False)
# print('\n✓ Saved: ../results/statistical_tests_intersection.csv')
#
# # ============================================================
# # Summary
# # ============================================================
#
# print('\n' + '='*80)
# print('EXTRACTION COMPLETE - SUMMARY')
# print('='*80)
#
# print(f'\nTotal configurations analyzed: 8')
# print(f'Total unique features: {len(all_features)}')
# print(f'Average features per config: {np.mean([len(d) for d in all_shap_data.values()]):.1f}')
#
# print('\nFiles Generated:')
# print('  1. shap_values_all_configs_intersection.csv - Complete SHAP data for all configs')
# print('  2. feature_importance_summary_intersection.csv - Feature frequency and importance summary')
# print('  3. ratiocommenttocode_analysis_intersection.csv - RatioCommentToCode analysis')
# print('  4. model_importance_statistics_intersection.csv - Model-level statistics')
# print('  5. feature_rankings_all_configs_intersection.csv - Complete rankings for all configs')
# print('  6. statistical_tests_intersection.csv - Statistical test results')
# print('  7. feature_importance_heatmap_intersection.pdf - Full heatmap')
# print('  8. feature_importance_heatmap_top10_intersection.pdf - Top 10 heatmap')
# print('  9. {llm}_{granularity}_catboost_shap_beeswarm_intersection.pdf - 8 beeswarm plots')
#
# print('\nKey Findings:')
# print(f'  - Top feature overall: {feature_summary_df.iloc[0]["Feature"]} (avg: {feature_summary_df.iloc[0]["Avg_Importance"]:.3f})')
# print(f'  - Most frequent feature: {feature_summary_df.sort_values("Frequency", ascending=False).iloc[0]["Feature"]} ({feature_summary_df.sort_values("Frequency", ascending=False).iloc[0]["Frequency"]}/8 configs)')
# print(f'  - Model with highest importance: {model_stats_df.iloc[0]["Model_Name"]} ({model_stats_df.iloc[0]["Overall_Mean"]:.3f})')
# if ratio_importance:
#     print(f'  - RatioCommentToCode appears in: {len(ratio_importance)}/8 configs')
#
# print('\n' + '='*80)
# print('DONE!')
# print('='*80)

"""
Extract SHAP values from trained CatBoost models and generate comprehensive analysis.
USING INTERSECTION DATA

This script:
1. Loads all 8 trained models (4 LLMs × 2 granularities) trained on intersection data
2. Computes SHAP values on test sets
3. Extracts mean absolute SHAP importance for each feature
4. Generates CSV files with actual SHAP data
5. Creates statistical analysis
6. Generates visualizations

Usage:
    python extract_shap_values_intersection.py
"""

import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import mannwhitneyu, permutation_test
import warnings
import os

warnings.filterwarnings('ignore')

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
    #'AvgCyclomaticModified': 'Average Modified Cyclomatic Complexity',
    'AvgCyclomaticStrict': 'Average Strict Cyclomatic Complexity',
    'MaxCyclomatic': 'Maximum Cyclomatic Complexity',
    'MaxCyclomaticModified': 'Maximum Modified Cyclomatic Complexity',
    'MaxCyclomaticStrict': 'Maximum Strict Cyclomatic Complexity',
    'MaxEssential': 'Maximum Essential Complexity',
    'SumCyclomatic': 'Sum Cyclomatic Complexity',
    'SumCyclomaticModified': 'Sum Modified Cyclomatic Complexity',
    'SumCyclomaticStrict': 'Sum Strict Cyclomatic Complexity',
    'SumEssential': 'Sum Essential Complexity',
    'AvgCyclomaticModified': 'Average Modified Cyclomatic Complexity',
}


def get_readable_name(feature):
    """Convert technical feature name to human-readable format."""
    return FEATURE_NAME_MAPPING.get(feature, feature)


# Configuration
MODELS = ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']
GRANULARITIES = ['Function', 'Class']
MODEL_NAMES = {
    'claude-3-haiku': 'Claude 3 Haiku',
    'claude-4-5-haiku': 'Claude 4.5 Haiku',
    'gpt-3-5': 'GPT-3.5',
    'gpt-oss': 'GPT-OSS'
}

# Output directories
os.makedirs('../results', exist_ok=True)
os.makedirs('../plots_for_paper', exist_ok=True)

print('=' * 80)
print('EXTRACTING SHAP VALUES FROM TRAINED MODELS (INTERSECTION DATA)')
print('=' * 80)

# ============================================================
# Step 1: Extract SHAP values from all models
# ============================================================

all_shap_data = {}
shap_summary = []

for llm in MODELS:
    for granularity in GRANULARITIES:
        config_key = f'{llm}_{granularity}'

        print(f'\nProcessing {MODEL_NAMES[llm]} {granularity}-level...')

        # Load model (intersection version)
        model_path = f'../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Load test data (intersection version)
        test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
        X_test = test_data.drop(columns=['label'])
        y_test = test_data['label']

        # Compute SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)

        # For binary classification, get positive class (LLM) SHAP values
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # Calculate mean absolute SHAP importance
        feature_importance = np.abs(shap_values).mean(axis=0)
        feature_names = X_test.columns.tolist()

        # Store for this configuration (using technical names as keys)
        importance_dict = dict(zip(feature_names, feature_importance))
        all_shap_data[config_key] = importance_dict

        # Create sorted dataframe with readable names
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Feature_Readable': [get_readable_name(f) for f in feature_names],
            'SHAP_Importance': feature_importance
        }).sort_values('SHAP_Importance', ascending=False)

        # Add to summary
        for rank, (idx, row) in enumerate(importance_df.iterrows(), 1):
            shap_summary.append({
                'Model': llm,
                'Model_Name': MODEL_NAMES[llm],
                'Granularity': granularity,
                'Config': config_key,
                'Feature': row['Feature'],
                'Feature_Readable': row['Feature_Readable'],
                'SHAP_Importance': row['SHAP_Importance'],
                'Rank': rank
            })

        print(f'  ✓ Extracted {len(feature_names)} features')
        print(f'  Top 3: {", ".join(importance_df.head(3)["Feature_Readable"].tolist())}')

print('\n✓ SHAP extraction complete for all 8 configurations')

# Save comprehensive SHAP data
shap_df = pd.DataFrame(shap_summary)
shap_df.to_csv('../results/shap_values_all_configs_intersection.csv', index=False)
print(f'\n✓ Saved: ../results/shap_values_all_configs_intersection.csv')

# ============================================================
# Step 2: Generate Beeswarm Plots for All Configurations
# ============================================================

print('\n' + '=' * 80)
print('GENERATING SHAP BEESWARM PLOTS')
print('=' * 80)

# Store SHAP values for later analysis
all_shap_values = {}
all_X_test = {}

for llm in MODELS:
    for granularity in GRANULARITIES:
        config_key = f'{llm}_{granularity}'

        print(f'\nGenerating beeswarm plot for {MODEL_NAMES[llm]} {granularity}-level...')

        # Load model and data again
        model_path = f'../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        test_data = pd.read_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')
        X_test = test_data.drop(columns=['label'])

        # Rename columns to human-readable names
        X_test_readable = X_test.rename(columns=FEATURE_NAME_MAPPING)

        # Compute SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)

        # For binary classification, get positive class (LLM)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # Store for later use
        all_shap_values[config_key] = shap_values
        all_X_test[config_key] = X_test

        # Create beeswarm plot with readable names
        fig, ax = plt.subplots(figsize=(12, 8))
        shap.summary_plot(shap_values, X_test_readable, show=False)  # Show ALL features

        # Add vertical line at 0
        ax.axvline(x=0, color='black', linestyle='-', linewidth=2, alpha=0.8, zorder=0)

        # Get current axis limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Add colored backgrounds
        ax.axvspan(xlim[0], 0, alpha=0.1, color='blue', zorder=0)
        ax.axvspan(0, xlim[1], alpha=0.1, color='red', zorder=0)

        # Add text labels
        ax.text(xlim[0] * 0.5, ylim[1] * 0.98, '← Human',
                fontsize=13, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7), weight='bold')
        ax.text(xlim[1] * 0.5, ylim[1] * 0.98, 'LLM →',
                fontsize=13, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7), weight='bold')

        ax.set_xlabel('SHAP Value (impact on model output)', fontsize=12, fontweight='bold')
        # Title removed as requested

        plt.tight_layout()

        # Save plot
        output_filename = f'../plots_for_paper/{llm}_{granularity}_catboost_shap_beeswarm_intersection.pdf'
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f'  ✓ Saved: {output_filename}')

print('\n✓ All beeswarm plots generated successfully')

# ============================================================
# Step 3: Generate Feature Importance Summary
# ============================================================

print('\n' + '=' * 80)
print('GENERATING FEATURE IMPORTANCE SUMMARY')
print('=' * 80)

# Get all unique features
all_features = set()
for config_data in all_shap_data.values():
    all_features.update(config_data.keys())

# Create frequency and importance summary
feature_summary = []
for feature in all_features:
    configs_present = []
    importances = []
    top3_count = 0

    for config_key, importance_dict in all_shap_data.items():
        if feature in importance_dict:
            configs_present.append(config_key)
            importances.append(importance_dict[feature])

            # Check if in top 3 for this config
            sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
            if feature in [f[0] for f in sorted_features[:3]]:
                top3_count += 1

    if importances:
        feature_summary.append({
            'Feature': feature,
            'Feature_Readable': get_readable_name(feature),
            'Frequency': len(configs_present),
            'Percentage': f'{len(configs_present) / 8 * 100:.0f}%',
            'Avg_Importance': np.mean(importances),
            'Max_Importance': np.max(importances),
            'Top3_Count': top3_count,
            'Configs': ', '.join(configs_present)
        })

feature_summary_df = pd.DataFrame(feature_summary).sort_values('Avg_Importance', ascending=False)
feature_summary_df.to_csv('../results/feature_importance_summary_intersection.csv', index=False)
print('✓ Saved: ../results/feature_importance_summary_intersection.csv')

print('\nTop 10 Features by Average Importance:')
print(feature_summary_df[['Feature_Readable', 'Frequency', 'Avg_Importance', 'Top3_Count']].head(10).to_string(
    index=False))

# ============================================================
# Step 4: Analyze RatioCommentToCode across configs
# ============================================================

print('\n' + '=' * 80)
print('ANALYZING RATIOCOMMENTTOCODE IMPORTANCE')
print('=' * 80)

ratio_importance = {}
for config_key, importance_dict in all_shap_data.items():
    if 'RatioCommentToCode' in importance_dict:
        ratio_importance[config_key] = importance_dict['RatioCommentToCode']

if ratio_importance:
    ratio_df = pd.DataFrame(list(ratio_importance.items()), columns=['Config', 'SHAP_Importance'])
    ratio_df['Model'] = ratio_df['Config'].apply(lambda x: x.rsplit('_', 1)[0])
    ratio_df['Granularity'] = ratio_df['Config'].apply(lambda x: x.rsplit('_', 1)[1])

    print('\nRatioCommentToCode (Comment-to-Code Ratio) SHAP Importance by Config:')
    for _, row in ratio_df.iterrows():
        print(f'  {row["Config"]:30s}: {row["SHAP_Importance"]:.4f}')

    # Function vs Class comparison
    func_values = ratio_df[ratio_df['Granularity'] == 'Function']['SHAP_Importance'].values
    class_values = ratio_df[ratio_df['Granularity'] == 'Class']['SHAP_Importance'].values

    if len(func_values) > 0 and len(class_values) > 0:
        print(f'\nFunction-level mean: {func_values.mean():.4f}')
        print(f'Class-level mean:    {class_values.mean():.4f}')
        print(f'Ratio (Func/Class):  {func_values.mean() / class_values.mean():.2f}x')


        # Permutation test
        def mean_diff(x, y, axis=-1):
            return np.mean(x, axis=axis) - np.mean(y, axis=axis)


        if len(func_values) >= 2 and len(class_values) >= 2:
            res = permutation_test((func_values, class_values), mean_diff,
                                   n_resamples=10000, alternative='two-sided')
            print(f'Permutation test p-value: {res.pvalue:.4f}')
            print(f'Significant: {"Yes" if res.pvalue < 0.05 else "No"}')
        else:
            print('Not enough data for permutation test')
            res = None
    else:
        print('RatioCommentToCode not found in enough configs for comparison')
        res = None

    ratio_df.to_csv('../results/ratiocommenttocode_analysis_intersection.csv', index=False)
    print('\n✓ Saved: ../results/ratiocommenttocode_analysis_intersection.csv')
else:
    print('\nRatioCommentToCode not found in any configuration')
    res = None

# ============================================================
# Step 5: Model-Specific Average Importance
# ============================================================

print('\n' + '=' * 80)
print('MODEL-SPECIFIC AVERAGE IMPORTANCE')
print('=' * 80)

model_stats = []
for llm in MODELS:
    func_config = f'{llm}_Function'
    class_config = f'{llm}_Class'

    func_importances = list(all_shap_data[func_config].values())
    class_importances = list(all_shap_data[class_config].values())

    model_stats.append({
        'Model': llm,
        'Model_Name': MODEL_NAMES[llm],
        'Function_Mean': np.mean(func_importances),
        'Function_Max': np.max(func_importances),
        'Class_Mean': np.mean(class_importances),
        'Class_Max': np.max(class_importances),
        'Overall_Mean': np.mean(func_importances + class_importances)
    })

model_stats_df = pd.DataFrame(model_stats).sort_values('Overall_Mean', ascending=False)
model_stats_df.to_csv('../results/model_importance_statistics_intersection.csv', index=False)
print('✓ Saved: ../results/model_importance_statistics_intersection.csv')

print('\nModel Importance Summary:')
print(model_stats_df[['Model_Name', 'Function_Mean', 'Class_Mean', 'Overall_Mean']].to_string(index=False))

# ============================================================
# Step 6: Top Feature Rankings
# ============================================================

print('\n' + '=' * 80)
print('TOP FEATURE RANKINGS BY CONFIGURATION')
print('=' * 80)

top_features_per_config = []
for config_key, importance_dict in all_shap_data.items():
    sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    llm, granularity = config_key.rsplit('_', 1)

    for rank, (feature, importance) in enumerate(sorted_features, 1):
        top_features_per_config.append({
            'Config': config_key,
            'Model': llm,
            'Model_Name': MODEL_NAMES[llm],
            'Granularity': granularity,
            'Rank': rank,
            'Feature': feature,
            'Feature_Readable': get_readable_name(feature),
            'SHAP_Importance': importance,
            'Is_Top3': 'Yes' if rank <= 3 else 'No'
        })

top_features_df = pd.DataFrame(top_features_per_config)
top_features_df.to_csv('../results/feature_rankings_all_configs_intersection.csv', index=False)
print('✓ Saved: ../results/feature_rankings_all_configs_intersection.csv')

# Show #1 feature for each config
print('\n#1 Feature by Configuration:')
rank1_df = top_features_df[top_features_df['Rank'] == 1]
for _, row in rank1_df.iterrows():
    print(f'  {row["Config"]:30s}: {row["Feature_Readable"]:35s} ({row["SHAP_Importance"]:.4f})')

# ============================================================
# Step 7: Generate Heatmap with ACTUAL Data (READABLE NAMES)
# ============================================================

print('\n' + '=' * 80)
print('GENERATING VISUALIZATIONS')
print('=' * 80)

# Create heatmap matrix with readable names
heatmap_data = {}
for config_key, importance_dict in all_shap_data.items():
    llm, granularity = config_key.rsplit('_', 1)
    for feature, importance in importance_dict.items():
        readable_feature = get_readable_name(feature)
        if readable_feature not in heatmap_data:
            heatmap_data[readable_feature] = {}
        col_name = f'{MODEL_NAMES[llm]}\n{granularity}'
        heatmap_data[readable_feature][col_name] = importance

heatmap_df = pd.DataFrame(heatmap_data).T.fillna(0)

# Reorder columns
column_order = []
for llm in MODELS:
    for gran in GRANULARITIES:
        col_name = f'{MODEL_NAMES[llm]}\n{gran}'
        if col_name in heatmap_df.columns:
            column_order.append(col_name)

heatmap_df = heatmap_df[column_order]

# Sort by max importance
heatmap_df['max_importance'] = heatmap_df.max(axis=1)
heatmap_df = heatmap_df.sort_values('max_importance', ascending=False)
heatmap_df = heatmap_df.drop('max_importance', axis=1)

# Create heatmap
fig, ax = plt.subplots(figsize=(14, 10))
cmap = LinearSegmentedColormap.from_list('custom',
                                         ['white', '#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'])

sns.heatmap(heatmap_df, annot=True, fmt='.3f', cmap=cmap,
            cbar_kws={'label': 'SHAP Importance'},
            linewidths=0.5, linecolor='gray', ax=ax,
            vmin=0, vmax=heatmap_df.max().max())

ax.set_title('Feature Importance Across Models and Granularities\n(SHAP Values - Intersection Data)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Model × Granularity', fontsize=13, fontweight='bold')
ax.set_ylabel('Feature', fontsize=13, fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Add vertical lines
for i in [2, 4, 6]:
    ax.axvline(x=i, color='black', linewidth=2)

plt.tight_layout()
plt.savefig('../plots_for_paper/feature_importance_heatmap_intersection.pdf', dpi=300, bbox_inches='tight')
print('✓ Saved: ../plots_for_paper/feature_importance_heatmap_intersection.pdf')

# Top 10 version
top10_df = heatmap_df.head(10)
fig, ax = plt.subplots(figsize=(12, 6))

sns.heatmap(top10_df, annot=True, fmt='.3f', cmap=cmap,
            cbar_kws={'label': 'SHAP Importance'},
            linewidths=0.5, linecolor='gray', ax=ax,
            vmin=0, vmax=heatmap_df.max().max())

ax.set_title('Top 10 Features: Importance Across Models and Granularities',
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Model × Granularity', fontsize=12, fontweight='bold')
ax.set_ylabel('Feature', fontsize=12, fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

for i in [2, 4, 6]:
    ax.axvline(x=i, color='black', linewidth=2)

plt.tight_layout()
plt.savefig('../plots_for_paper/feature_importance_heatmap_top10_intersection.pdf', dpi=300, bbox_inches='tight')
print('✓ Saved: ../plots_for_paper/feature_importance_heatmap_top10_intersection.pdf')

# ============================================================
# Step 8: Statistical Tests
# ============================================================

print('\n' + '=' * 80)
print('STATISTICAL TESTS')
print('=' * 80)

statistical_tests = []

# Test 1: Overall distribution comparison (Function vs Class)
all_func_importance = []
all_class_importance = []

for config_key, importance_dict in all_shap_data.items():
    granularity = config_key.rsplit('_', 1)[1]
    if granularity == 'Function':
        all_func_importance.extend(importance_dict.values())
    else:
        all_class_importance.extend(importance_dict.values())

u_stat, p_val = mannwhitneyu(all_func_importance, all_class_importance, alternative='two-sided')


def cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(
        ((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / dof)


effect_size = cohens_d(all_func_importance, all_class_importance)

statistical_tests.append({
    'Test': 'Mann-Whitney U',
    'Comparison': 'Function vs Class (All Features)',
    'Statistic': u_stat,
    'P-value': p_val,
    'Effect_Size': effect_size,
    'Interpretation': 'Negligible' if abs(effect_size) < 0.2 else 'Small' if abs(
        effect_size) < 0.5 else 'Medium' if abs(effect_size) < 0.8 else 'Large'
})

print(f'\nMann-Whitney U Test (Function vs Class):')
print(f'  U-statistic: {u_stat:.2f}')
print(f'  p-value: {p_val:.4f}')
print(f'  Cohen\'s d: {effect_size:.4f}')

# Test 2: RatioCommentToCode Function vs Class (if available)
if res is not None and ratio_importance:
    statistical_tests.append({
        'Test': 'Permutation Test',
        'Comparison': 'RatioCommentToCode: Function vs Class',
        'Statistic': func_values.mean() - class_values.mean(),
        'P-value': res.pvalue,
        'Effect_Size': func_values.mean() / class_values.mean(),
        'Interpretation': f'{func_values.mean() / class_values.mean():.1f}x higher at function-level'
    })

stats_df = pd.DataFrame(statistical_tests)
stats_df.to_csv('../results/statistical_tests_intersection.csv', index=False)
print('\n✓ Saved: ../results/statistical_tests_intersection.csv')

# ============================================================
# Summary
# ============================================================

print('\n' + '=' * 80)
print('EXTRACTION COMPLETE - SUMMARY')
print('=' * 80)

print(f'\nTotal configurations analyzed: 8')
print(f'Total unique features: {len(all_features)}')
print(f'Average features per config: {np.mean([len(d) for d in all_shap_data.values()]):.1f}')

print('\nFiles Generated:')
print('  1. shap_values_all_configs_intersection.csv - Complete SHAP data for all configs')
print('  2. feature_importance_summary_intersection.csv - Feature frequency and importance summary')
print('  3. ratiocommenttocode_analysis_intersection.csv - RatioCommentToCode analysis')
print('  4. model_importance_statistics_intersection.csv - Model-level statistics')
print('  5. feature_rankings_all_configs_intersection.csv - Complete rankings for all configs')
print('  6. statistical_tests_intersection.csv - Statistical test results')
print('  7. feature_importance_heatmap_intersection.pdf - Full heatmap')
print('  8. feature_importance_heatmap_top10_intersection.pdf - Top 10 heatmap')
print('  9. {llm}_{granularity}_catboost_shap_beeswarm_intersection.pdf - 8 beeswarm plots')

print('\nKey Findings:')
print(
    f'  - Top feature overall: {feature_summary_df.iloc[0]["Feature_Readable"]} (avg: {feature_summary_df.iloc[0]["Avg_Importance"]:.3f})')
print(
    f'  - Most frequent feature: {feature_summary_df.sort_values("Frequency", ascending=False).iloc[0]["Feature_Readable"]} ({feature_summary_df.sort_values("Frequency", ascending=False).iloc[0]["Frequency"]}/8 configs)')
print(
    f'  - Model with highest importance: {model_stats_df.iloc[0]["Model_Name"]} ({model_stats_df.iloc[0]["Overall_Mean"]:.3f})')
if ratio_importance:
    print(f'  - Comment-to-Code Ratio appears in: {len(ratio_importance)}/8 configs')

print('\n' + '=' * 80)
print('DONE!')
print('=' * 80)
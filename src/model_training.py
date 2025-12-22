import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
import warnings
from sklearn.exceptions import ConvergenceWarning
import pickle
import sys
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import numpy as np
from sklearn.metrics import roc_auc_score, confusion_matrix, precision_score, recall_score, f1_score, matthews_corrcoef
from sklearn.model_selection import cross_val_score
# Import for Construct Defect Models (Classification)
from sklearn.linear_model import LogisticRegression  # Logistic Regression
from sklearn.ensemble import RandomForestClassifier  # Random Forests
from sklearn.neural_network import MLPClassifier  # Neural Network
from sklearn.svm import SVC
import xgboost as xgb  # eXtreme Gradient Boosting Tree (xGBTree)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from catboost import CatBoostClassifier


# taken from https://xai4se.github.io/defect-prediction/data-preprocessing.html
def AutoSpearman(X_train, correlation_threshold=0.7, correlation_method='spearman', VIF_threshold=5):
    X_AS_train = X_train.copy()
    AS_metrics = X_AS_train.columns
    count = 1

    # (Part 1) Automatically select non-correlated metrics based on a Spearman rank correlation test.
    print('(Part 1) Automatically select non-correlated metrics based on a Spearman rank correlation test')
    while True:
        corrmat = X_AS_train.corr(method=correlation_method)
        top_corr_features = corrmat.index
        abs_corrmat = abs(corrmat)

        # identify correlated metrics with the correlation threshold of the threshold
        highly_correlated_metrics = ((corrmat > correlation_threshold) | (corrmat < -correlation_threshold)) & (
                corrmat != 1)
        n_correlated_metrics = np.sum(np.sum(highly_correlated_metrics))
        if n_correlated_metrics > 0:
            # find the strongest pair-wise correlation
            find_top_corr = pd.melt(abs_corrmat, ignore_index=False)
            find_top_corr.reset_index(inplace=True)
            find_top_corr = find_top_corr[find_top_corr['value'] != 1]
            top_corr_index = find_top_corr['value'].idxmax()
            top_corr_i = find_top_corr.loc[top_corr_index, :]

            # get the 2 correlated metrics with the strongest correlation
            correlated_metric_1 = top_corr_i[0]
            correlated_metric_2 = top_corr_i[1]
            print('> Step', count, 'comparing between', correlated_metric_1, 'and', correlated_metric_2)

            # compute their correlation with other metrics outside of the pair
            correlation_with_other_metrics_1 = np.mean(abs_corrmat[correlated_metric_1][[i for i in top_corr_features if
                                                                                         i not in [correlated_metric_1,
                                                                                                   correlated_metric_2]]])
            correlation_with_other_metrics_2 = np.mean(abs_corrmat[correlated_metric_2][[i for i in top_corr_features if
                                                                                         i not in [correlated_metric_1,
                                                                                                   correlated_metric_2]]])
            print('>>', correlated_metric_1, 'has the average correlation of',
                  np.round(correlation_with_other_metrics_1, 3), 'with other metrics')
            print('>>', correlated_metric_2, 'has the average correlation of',
                  np.round(correlation_with_other_metrics_2, 3), 'with other metrics')
            # select the metric that shares the least correlation outside of the pair and exclude the other
            if correlation_with_other_metrics_1 < correlation_with_other_metrics_2:
                exclude_metric = correlated_metric_2
            else:
                exclude_metric = correlated_metric_1
            print('>>', 'Exclude', exclude_metric)
            count = count + 1
            AS_metrics = list(set(AS_metrics) - set([exclude_metric]))
            X_AS_train = X_AS_train[AS_metrics]
        else:
            break

    print('According to Part 1 of AutoSpearman,', AS_metrics, 'are selected.')

    # (Part 2) Automatically select non-correlated metrics based on a Variance Inflation Factor analysis.
    print('(Part 2) Automatically select non-correlated metrics based on a Variance Inflation Factor analysis')

    # Prepare a dataframe for VIF
    X_AS_train = add_constant(X_AS_train)

    # Check for inf values and drop those columns
    inf_mask = np.isinf(X_AS_train).any()
    inf_cols = X_AS_train.columns[inf_mask].tolist()
    if inf_cols:
        print(f'  Dropping columns with inf before VIF: {inf_cols}')
        X_AS_train = X_AS_train.drop(columns=inf_cols)

    # Drop constant columns
    constant_cols = X_AS_train.columns[X_AS_train.std() == 0].tolist()
    if constant_cols:
        print(f'  Dropping constant columns before VIF: {constant_cols}')
        X_AS_train = X_AS_train.drop(columns=constant_cols)

    selected_features = X_AS_train.columns
    count = 1
    while True:
        try:
            # Calculate VIF scores
            vif_scores = pd.DataFrame([variance_inflation_factor(X_AS_train.values, i)
                                       for i in range(X_AS_train.shape[1])],
                                      index=X_AS_train.columns)
        except Exception as e:
            print(f'  VIF calculation failed: {e}')
            print(f'  Skipping VIF analysis, using features from Spearman correlation only')
            break

        # Prepare a final dataframe of VIF scores
        vif_scores.reset_index(inplace=True)
        vif_scores.columns = ['Feature', 'VIFscore']
        vif_scores = vif_scores.loc[vif_scores['Feature'] != 'const', :]
        vif_scores.sort_values(by=['VIFscore'], ascending=False, inplace=True)

        # Find features that have their VIF scores of above the threshold
        filtered_vif_scores = vif_scores[vif_scores['VIFscore'] >= VIF_threshold]

        # Terminate when there is no features with the VIF scores of above the threshold
        if len(filtered_vif_scores) == 0:
            break

        # exclude the metric with the highest VIF score
        metric_to_exclude = list(filtered_vif_scores['Feature'].head(1))[0]

        print('> Step', count, '- exclude', str(metric_to_exclude))
        count = count + 1

        selected_features = list(set(selected_features) - set([metric_to_exclude]))

        X_AS_train = X_AS_train.loc[:, selected_features]

    print('Finally, according to Part 2 of AutoSpearman,', list(set(selected_features) - set(['const'])),
          'are selected.')
    return list(set(selected_features) - set(['const']))


def load_and_process_intersection_data(human_file, llm_file):
    """
    Load pre-aligned intersection data and prepare for ML.
    No inner join needed - data is already matched.

    Args:
        human_file: Path to human intersection CSV
        llm_file: Path to LLM intersection CSV

    Returns:
        X_train, X_test, y_train, y_test, final_features
    """
    print('\n' + '=' * 60)
    print('DATA PREPROCESSING (INTERSECTION DATA)')
    print('=' * 60)

    # Load intersection data
    human_df = pd.read_csv(human_file, low_memory=False)
    llm_df = pd.read_csv(llm_file, low_memory=False)

    print(f'\nLoaded intersection data:')
    print(f'  Human samples: {len(human_df)}')
    print(f'  LLM samples: {len(llm_df)}')

    # Verify alignment
    if len(human_df) != len(llm_df):
        raise ValueError(f"Mismatched lengths: human={len(human_df)}, llm={len(llm_df)}")

    if 'composite_key' in human_df.columns and 'composite_key' in llm_df.columns:
        if list(human_df['composite_key']) != list(llm_df['composite_key']):
            raise ValueError("Composite keys don't match - data not properly aligned!")
        print('✓ Verified: Data is properly aligned via composite keys')

    # Identify feature columns (exclude metadata)
    metadata_cols = ['Kind', 'Name', 'File', 'BaseFile', 'composite_key']
    feature_cols = [col for col in human_df.columns if col not in metadata_cols]

    print(f'\nFound {len(feature_cols)} feature columns')

    # Create labeled datasets
    human_features = human_df[feature_cols].copy()
    human_features['label'] = 0

    llm_features = llm_df[feature_cols].copy()
    llm_features['label'] = 1

    # Combine datasets
    combined = pd.concat([human_features, llm_features], ignore_index=True)

    print(f'\nCombined dataset shape: {combined.shape}')
    print(f'  Human samples: {(combined["label"] == 0).sum()}')
    print(f'  LLM samples: {(combined["label"] == 1).sum()}')

    # Separate features and labels
    X = combined.drop(columns=['label'])
    y = combined['label'].values

    # Handle missing and problematic values
    print(f'\nHandling missing and problematic values...')

    # Drop columns with any NaN values
    nan_cols = X.columns[X.isna().any()].tolist()
    if nan_cols:
        print(f'  Dropping columns with NaN: {nan_cols}')
        X = X.drop(columns=nan_cols)

    # Replace inf with NaN, then drop those columns
    inf_mask = np.isinf(X).any()
    inf_cols = X.columns[inf_mask].tolist()
    if inf_cols:
        print(f'  Dropping columns with inf: {inf_cols}')
        X = X.drop(columns=inf_cols)

    # Drop constant columns (std = 0)
    constant_cols = X.columns[X.std() == 0].tolist()
    if constant_cols:
        print(f'  Dropping constant columns: {constant_cols}')
        X = X.drop(columns=constant_cols)

    print(f'  Final feature count: {X.shape[1]} features')

    # Train-test split with stratification
    print(f'\nPerforming 80/20 train-test split with stratification...')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f'  Training set: {len(X_train)} samples (Human: {(y_train == 0).sum()}, LLM: {(y_train == 1).sum()})')
    print(f'  Test set: {len(X_test)} samples (Human: {(y_test == 0).sum()}, LLM: {(y_test == 1).sum()})')

    # AutoSpearman feature selection on training data only
    print('\n' + '=' * 60)
    print('AUTOSPEARMAN FEATURE SELECTION')
    print('=' * 60)
    final_features = AutoSpearman(X_train)

    print(f'\n✓ Selected {len(final_features)} features after AutoSpearman:')
    print(f'  {final_features}')

    # Apply feature selection to both train and test
    X_train = X_train[final_features]
    X_test = X_test[final_features]

    return X_train, X_test, y_train, y_test, final_features


def perform_models_selection(X_train, y_train):
    cv_kfold = 10
    cv_repetitions = 30  # 30 repetitions for robust statistics
    model_performance_list = []

    print('\n' + '=' * 60)
    print('MODEL SELECTION PHASE')
    print('=' * 60)
    print(f"Running {cv_repetitions} repetitions of {cv_kfold}-fold CV...")
    print(f"Total evaluations per model: {cv_repetitions * cv_kfold} = {cv_repetitions * cv_kfold}")
    print('=' * 60)

    ## Construct defect models and generate repeated 10-fold Cross Validation AUC

    for rep in range(cv_repetitions):
        print(f"\n--- Repetition {rep + 1}/{cv_repetitions} ---")

        # Logistic Regression
        print("Training Logistic Regression...")
        lr_model = LogisticRegression(random_state=1234 + rep, n_jobs=-1, max_iter=10000)
        lr_scores = cross_val_score(lr_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # Naive Bayes
        print("Training Naive Bayes...")
        nb_model = GaussianNB()
        nb_scores = cross_val_score(nb_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # KNN
        print("Training KNN...")
        knn_model = KNeighborsClassifier(n_jobs=-1)
        knn_scores = cross_val_score(knn_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # SVM
        print("Training SVM...")
        svc_model = SVC(random_state=1234 + rep, max_iter=10000, probability=True)
        svm_scores = cross_val_score(svc_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # Random Forests
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(random_state=1234 + rep, n_jobs=-1)
        rf_scores = cross_val_score(rf_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # eXtreme Gradient Boosting Tree (XGBoost)
        print("Training XGBoost...")
        xgb_model = xgb.XGBClassifier(random_state=1234 + rep, n_jobs=-1, tree_method='hist')
        xgb_scores = cross_val_score(xgb_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # CatBoost
        print("Training CatBoost...")
        catboost_model = CatBoostClassifier(random_state=1234 + rep, verbose=0, thread_count=-1)
        catboost_scores = cross_val_score(catboost_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # Neural Network
        print("Training Neural Network...")
        nn_model = MLPClassifier(random_state=1234 + rep, max_iter=10000)
        nn_scores = cross_val_score(nn_model, X_train, y_train, cv=cv_kfold, scoring='roc_auc', n_jobs=-1)

        # Store scores for this repetition
        for i in range(cv_kfold):
            model_performance_list.append({
                'Repetition': rep + 1,
                'Fold': i + 1,
                'LR': lr_scores[i],
                'NB': nb_scores[i],
                'KNN': knn_scores[i],
                'SVM': svm_scores[i],
                'RF': rf_scores[i],
                'XGB': xgb_scores[i],
                'CatBoost': catboost_scores[i],
                'MLP': nn_scores[i]
            })

    # Convert to DataFrame
    model_performance_df = pd.DataFrame(model_performance_list)

    print("\n✓ All models trained!")

    return model_performance_df


def bootstrap_evaluate(model, X_test, y_test, n_bootstrap=1000):
    """
    Evaluate model performance with bootstrap confidence intervals.

    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        n_bootstrap: Number of bootstrap iterations (default 1000)

    Returns:
        Dictionary with mean, std, and CI for all metrics
    """
    print(f'\n{"=" * 60}')
    print('BOOTSTRAP EVALUATION FOR STATISTICAL ROBUSTNESS')
    print(f'{"=" * 60}')
    print(f'Running {n_bootstrap} bootstrap iterations on test set (n={len(y_test)})...\n')

    # Convert to numpy arrays for faster indexing
    X_test_arr = np.array(X_test)
    y_test_arr = np.array(y_test)

    # Store bootstrap results
    bootstrap_metrics = {
        'auc': [],
        'precision': [],
        'recall': [],
        'f1': [],
        'mcc': []
    }

    # Bootstrap iterations
    for i in range(n_bootstrap):
        if (i + 1) % 100 == 0:
            print(f'  Completed {i + 1}/{n_bootstrap} iterations...')

        # Resample with replacement
        indices = np.random.choice(len(y_test_arr), size=len(y_test_arr), replace=True)
        X_boot = X_test_arr[indices]
        y_boot = y_test_arr[indices]

        # Get predictions
        y_pred = model.predict(X_boot)
        y_pred_proba = model.predict_proba(X_boot)[:, 1]

        # Calculate metrics
        try:
            bootstrap_metrics['auc'].append(roc_auc_score(y_boot, y_pred_proba))
            bootstrap_metrics['precision'].append(precision_score(y_boot, y_pred, zero_division=0))
            bootstrap_metrics['recall'].append(recall_score(y_boot, y_pred, zero_division=0))
            bootstrap_metrics['f1'].append(f1_score(y_boot, y_pred, zero_division=0))
            bootstrap_metrics['mcc'].append(matthews_corrcoef(y_boot, y_pred))
        except:
            # Skip this iteration if metrics fail (e.g., all same class in bootstrap sample)
            continue

    print(f'\n✓ Bootstrap complete! Computed {len(bootstrap_metrics["auc"])} valid samples.\n')

    # Compute statistics for each metric
    results = {}
    for metric_name, values in bootstrap_metrics.items():
        values_arr = np.array(values)
        results[metric_name] = {
            'mean': np.mean(values_arr),
            'std': np.std(values_arr),
            'ci_lower': np.percentile(values_arr, 2.5),
            'ci_upper': np.percentile(values_arr, 97.5),
            'median': np.median(values_arr)
        }

    return results


def train_best_model(X_train, X_test, y_train, y_test):
    """Train CatBoost and evaluate with both single-point and bootstrap metrics."""

    print('\n' + '=' * 60)
    print('TRAINING FINAL MODEL (CatBoost)')
    print('=' * 60)

    final_catboost_model = CatBoostClassifier(random_state=1234, verbose=0, thread_count=-1)
    final_catboost_model.fit(X_train, y_train)

    print('\n--- Single-Point Evaluation on Test Set ---')

    # Construct a confusion matrix
    print('\nConfusion Matrix:')
    tn, fp, fn, tp = confusion_matrix(y_test, final_catboost_model.predict(X_test)).ravel()
    print(f'(True Positive, False Positive) = ({tp}, {fp})')
    print(f'(False Negative, True Negative) = ({fn}, {tn})\n')

    # Calculate single-point metrics
    y_pred = final_catboost_model.predict(X_test)
    y_pred_proba = final_catboost_model.predict_proba(X_test)[:, 1]

    single_point_metrics = {
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'auc': roc_auc_score(y_test, y_pred_proba),
        'mcc': matthews_corrcoef(y_test, y_pred)
    }

    print('Single-Point Metrics:')
    print(f"  Precision: {single_point_metrics['precision']:.4f}")
    print(f"  Recall:    {single_point_metrics['recall']:.4f}")
    print(f"  F1:        {single_point_metrics['f1']:.4f}")
    print(f"  AUC:       {single_point_metrics['auc']:.4f}")
    print(f"  MCC:       {single_point_metrics['mcc']:.4f}")

    # Bootstrap evaluation for statistical robustness
    bootstrap_results = bootstrap_evaluate(final_catboost_model, X_test, y_test, n_bootstrap=1000)

    # Print bootstrap results
    print('=' * 60)
    print('BOOTSTRAP RESULTS (Publication-Ready Metrics)')
    print('=' * 60)
    print('\nFormat: Mean ± Std [95% CI Lower, 95% CI Upper]\n')

    for metric_name in ['auc', 'precision', 'recall', 'f1', 'mcc']:
        stats = bootstrap_results[metric_name]
        print(f"{metric_name.upper():10s}: {stats['mean']:.4f} ± {stats['std']:.4f} "
              f"[{stats['ci_lower']:.4f}, {stats['ci_upper']:.4f}]")

    # Save bootstrap results to file
    bootstrap_df = pd.DataFrame({
        'metric': list(bootstrap_results.keys()),
        'mean': [v['mean'] for v in bootstrap_results.values()],
        'std': [v['std'] for v in bootstrap_results.values()],
        'ci_lower': [v['ci_lower'] for v in bootstrap_results.values()],
        'ci_upper': [v['ci_upper'] for v in bootstrap_results.values()],
        'median': [v['median'] for v in bootstrap_results.values()]
    })

    return final_catboost_model, single_point_metrics, bootstrap_results, bootstrap_df


if __name__ == '__main__':
    warnings.filterwarnings('ignore', category=ConvergenceWarning)

    llm = sys.argv[1]
    granularity = sys.argv[2]

    print(f'\n{"=" * 80}')
    print(f'PROCESSING: {llm.upper()} - {granularity.upper()} LEVEL')
    print(f'USING GLOBAL INTERSECTION DATA')
    print(f'{"=" * 80}\n')

    # Load intersection data - already pre-aligned
    print(f'Loading intersection data from: ../data/features_for_ML/{granularity.lower()}_global_intersection/')
    human_file = f"../data/features_for_ML/{granularity.lower()}_global_intersection/human/human_intersection.csv"
    llm_file = f"../data/features_for_ML/{granularity.lower()}_global_intersection/{llm}/{llm}_intersection.csv"

    # Load and process intersection data (no inner join needed - already matched)
    X_train, X_test, y_train, y_test, final_features = load_and_process_intersection_data(
        human_file, llm_file
    )

    # Save test data for future validation
    df_test = X_test.copy()
    df_test['label'] = y_test
    df_test.to_csv(f'../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv', index=False)
    print(f'\n✓ Test data saved to: ../data/data_for_ML_validation/{llm}_{granularity}_test_data_intersection.csv')

    # Save selected features
    features_df = pd.DataFrame({'feature': final_features})
    features_df.to_csv(f'../results/selected_features_{granularity}_{llm}_intersection.csv', index=False)
    print(f'✓ Selected features saved to: ../results/selected_features_{granularity}_{llm}_intersection.csv')

    # Perform model selection
    model_performance_df = perform_models_selection(X_train, y_train)

    # Export to csv
    model_performance_df.to_csv(f'../results/model_performance_{granularity}_{llm}_intersection.csv', index=False)
    print(f'\n✓ Model performance saved to: ../results/model_performance_{granularity}_{llm}_intersection.csv')

    # Display summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS (30x10-fold CV)")
    print("=" * 60)
    summary_stats = model_performance_df.drop(columns=['Repetition', 'Fold']).describe()
    print(summary_stats)

    print("\n" + "=" * 60)
    print("MEDIAN AUC PER MODEL (Sorted)")
    print("=" * 60)
    median_scores = model_performance_df.drop(columns=['Repetition', 'Fold']).median().sort_values(ascending=False)
    print(median_scores)

    # Train final model and get bootstrap results
    best_model, single_metrics, bootstrap_results, bootstrap_df = train_best_model(X_train, X_test, y_train, y_test)

    # Save bootstrap results
    bootstrap_df.to_csv(f'../results/bootstrap_results_{granularity}_{llm}_intersection.csv', index=False)
    print(f'\n✓ Bootstrap results saved to: ../results/bootstrap_results_{granularity}_{llm}_intersection.csv')

    # Save the model to a file
    filename = f'../data/trained_ML_models/{granularity}_{llm}_finalized_model_intersection.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(best_model, file)

    print(f'✓ Model saved to: {filename}')

    print('\n' + '=' * 80)
    print('COMPLETE!')
    print('=' * 80)
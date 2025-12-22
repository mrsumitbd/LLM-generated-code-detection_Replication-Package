import matplotlib.pyplot as plt
import numpy as np

def plot_ranked_auc(uq_result, correct_indicators, scorers_names=None, write_path=None, title="Hallucination Detection: Scorer-specific AUROC", fontsize=10, fontname=None, metric_type="auroc", baseline=0.5):
    if scorers_names is None:
        scorers_names = uq_result.scorers

    if metric_type == "auroc":
        scores = uq_result.auroc_scores
        ylabel = "AUROC"
    elif metric_type == "auprc":
        scores = uq_result.auprc_scores
        ylabel = "AUPRC"
    else:
        scores = [uq_result.auroc_scores, uq_result.auprc_scores]
        ylabel = ["AUROC", "AUPRC"]

    sorted_indices = np.argsort(scores)[::-1]
    sorted_scores = np.array(scores)[sorted_indices]
    sorted_names = [scorers_names[i] for i in sorted_indices]

    plt.figure(figsize=(12, 6))
    plt.barh(sorted_names, sorted_scores, color='skyblue')
    plt.axvline(x=baseline, color='r', linestyle='--')
    plt.xlabel(ylabel)
    plt.ylabel('Scorers')
    plt.title(title)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    if fontname:
        plt.rcParams['font.family'] = fontname

    if write_path:
        plt.savefig(write_path)
    plt.show()
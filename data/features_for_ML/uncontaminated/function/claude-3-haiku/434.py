import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from sklearn.metrics import roc_auc_score, average_precision_score
from uq_result import UQResult
from typing import ArrayLike

def plot_ranked_auc(uq_result: UQResult, correct_indicators: ArrayLike, scorers_names: List[str] = None, write_path: Optional[str] = None, title: str = "Hallucination Detection: Scorer-specific AUROC", fontsize: int = 10, fontname: str = None, metric_type="auroc", baseline: float = 0.5):
    if metric_type == "auroc":
        scores = [roc_auc_score(correct_indicators, uq_result.get_scores(scorer)) for scorer in uq_result.scorers]
        metric_name = "AUROC"
    elif metric_type == "auprc":
        scores = [average_precision_score(correct_indicators, uq_result.get_scores(scorer)) for scorer in uq_result.scorers]
        metric_name = "AUPRC"
    elif metric_type == "both":
        auroc_scores = [roc_auc_score(correct_indicators, uq_result.get_scores(scorer)) for scorer in uq_result.scorers]
        auprc_scores = [average_precision_score(correct_indicators, uq_result.get_scores(scorer)) for scorer in uq_result.scorers]
        scores = [auroc_scores, auprc_scores]
        metric_name = ["AUROC", "AUPRC"]
    else:
        raise ValueError("Invalid metric_type. Must be 'auroc', 'auprc', or 'both'.")

    if scorers_names is None:
        scorers_names = uq_result.scorers

    if metric_type == "both":
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for i, ax in enumerate(axes):
            ax.bar(np.arange(len(scores[i])), scores[i])
            ax.axhline(y=baseline, color='r', linestyle='--')
            ax.set_xticks(np.arange(len(scores[i])))
            ax.set_xticklabels(scorers_names, rotation=90, fontsize=fontsize, fontname=fontname)
            ax.set_title(f"{metric_name[i]}", fontsize=fontsize, fontname=fontname)
            ax.set_ylabel(metric_name[i], fontsize=fontsize, fontname=fontname)
    else:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(np.arange(len(scores)), scores)
        ax.axhline(y=baseline, color='r', linestyle='--')
        ax.set_xticks(np.arange(len(scores)))
        ax.set_xticklabels(scorers_names, rotation=90, fontsize=fontsize, fontname=fontname)
        ax.set_title(title, fontsize=fontsize, fontname=fontname)
        ax.set_ylabel(metric_name, fontsize=fontsize, fontname=fontname)

    plt.tight_layout()
    if write_path:
        plt.savefig(write_path)
    else:
        plt.show()
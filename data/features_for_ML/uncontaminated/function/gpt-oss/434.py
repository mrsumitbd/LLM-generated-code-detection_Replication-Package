import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
from sklearn.metrics import roc_auc_score, average_precision_score

def plot_ranked_auc(
    uq_result,
    correct_indicators,
    scorers_names: List[str] = None,
    write_path: Optional[str] = None,
    title: str = "Hallucination Detection: Scorer-specific AUROC",
    fontsize: int = 10,
    fontname: str = None,
    metric_type: str = "auroc",
    baseline: float = 0.5,
):
    """
    Plot the ranked bar plot for hallucination detection AUROC/AUPRC of the given scorers.

    Parameters
    ----------
    uq_result : UQResult
        The UQResult object to plot

    correct_indicators : ArrayLike
        The correct indicators of the responses

    scorers_names : List[str], default=None
        The names of the scorers to plot

    title : str, default="Hallucination Detection: Scorer-specific AUROC"
        The title of the plot. Adjusted based on the metric type

    write_path : Optional[str], default=None
        The path to save the plot

    fontsize : int, default=10
        The font size of the plot

    fontname : str, default=None
        The font name of the plot

    metric_type: str, default="auroc"
        Type of metric(s) to compute and plot:
       - "auroc": Plot only AUROC scores (Area Under ROC Curve)
       - "auprc": Plot only AUPRC scores (Area Under Precision-Recall Curve)
       - "both": Plot both AUROC and AUPRC side by side in subplots

    baseline: float, default=0.5
        The baseline value to show as a dotted line (typically 0.5 for AUROC)

    Returns
    -------
    None
    """
    # Ensure correct_indicators is a numpy array
    y_true = np.asarray(correct_indicators)

    # Extract scorer names and scores from uq_result
    if scorers_names is None:
        if hasattr(uq_result, "scorer_names"):
            scorers_names = list(uq_result.scorer_names)
        elif hasattr(uq_result, "scores"):
            scorers_names = list(uq_result.scores.keys())
        else:
            raise ValueError("uq_result does not contain scorer names or scores.")

    # Retrieve scores for each scorer
    scores_dict = {}
    if hasattr(uq_result, "scores"):
        scores_dict = uq_result.scores
    else:
        # Try to get attributes dynamically
        for name in scorers_names:
            if hasattr(uq_result, name):
                scores_dict[name] = getattr(uq_result, name)
            else:
                raise AttributeError(f"uq_result has no attribute for scorer '{name}'.")

    # Compute metrics
    metrics = {}
    for name in scorers_names:
        scores = np.asarray(scores_dict[name])
        if metric_type in ("auroc", "both"):
            try:
                auc = roc_auc_score(y_true, scores)
            except ValueError:
                auc = np.nan
            metrics.setdefault(name, {})["auroc"] = auc
        if metric_type in ("auprc", "both"):
            try:
                aprc = average_precision_score(y_true, scores)
            except ValueError:
                aprc = np.nan
            metrics.setdefault(name, {})["auprc"] = aprc

    # Prepare plotting
    if fontname:
        plt.rcParams["font.family"] = fontname

    if metric_type == "both":
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        metric_titles = {"auroc": "AUROC", "auprc": "AUPRC"}
        for ax, mtype in zip(axes, ["auroc", "auprc"]):
            # Sort scorers by metric
            sorted_items = sorted(
                [(name, metrics[name][mtype]) for name in scorers_names],
                key=lambda x: (np.isnan(x[1]), -x[1]),
            )
            names, values = zip(*sorted_items)
            ax.barh(names, values, color="steelblue")
            ax.set_xlabel(metric_titles[mtype], fontsize=fontsize)
            ax.set_ylabel("Scorer", fontsize=fontsize)
            ax.tick_params(axis="both", which="major", labelsize=fontsize)
            ax.axvline(baseline, color="k", linestyle="--")
            ax.set_title(f"{metric_titles[mtype]} Ranking", fontsize=fontsize + 2)
        fig.suptitle(title, fontsize=fontsize + 4)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    else:
        mtype = metric_type
        sorted_items = sorted(
            [(name, metrics[name][mtype]) for name in scorers_names],
            key=lambda x: (np.isnan(x[1]), -x[1]),
        )
        names, values = zip(*sorted_items)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(names, values, color="steelblue")
        ax.set_xlabel(mtype.upper(), fontsize=fontsize)
        ax.set_ylabel("Scorer", fontsize=fontsize)
        ax.tick_params(axis="both", which="major", labelsize=fontsize)
        ax.axvline(baseline, color="k", linestyle="--")
        ax.set_title(f"{mtype.upper()} Ranking", fontsize=fontsize + 2)
        fig.suptitle(title, fontsize=fontsize + 4)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save or show
    if write_path:
        plt.savefig(write_path, bbox_inches="tight")
    plt.close(fig)
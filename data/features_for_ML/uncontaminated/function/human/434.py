import matplotlib.pyplot as plt
from typing import List, Optional
from numpy.typing import ArrayLike
from sklearn.metrics import roc_auc_score, average_precision_score
from uqlm.utils.results import UQResult

def plot_ranked_auc(uq_result: UQResult, correct_indicators: ArrayLike, scorers_names: List[str] = None, write_path: Optional[str] = None, title: str = "Hallucination Detection: Scorer-specific AUROC", fontsize: int = 10, fontname: str = None, metric_type="auroc", baseline: float = 0.5):
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
    bar_colors: list = ["C0", "C2", "C3", "C4"]

    if correct_indicators is None:
        raise ValueError("correct_indicators must be provided")
    if len(correct_indicators) != len(uq_result.data["responses"]):
        raise ValueError("correct_responses must be the same length as the number of responses")

    if scorers_names is None:
        scorers_names = [col for col in uq_result.data.keys() if col not in Ignore_Columns]

    if metric_type not in ["auroc", "auprc", "both"]:
        raise ValueError("metric_type must be one of 'both', 'auroc', 'auprc'")

    # Determine which metrics to compute
    metrics = ["auroc", "auprc"] if metric_type == "both" else [metric_type]

    # Initialize score dictionaries for each metric
    scores = {}
    for metric in metrics:
        scores[metric] = {"Black-box": {}, "White-box": {}, "Judges": {}, "Ensemble": {}}

    if metric_type in ["both", "auprc"]:
        # For AUPRC, we need flipped labels
        incorrect_indicators = [not ci for ci in correct_indicators]

    for col in scorers_names:
        if col in uq_result.data.keys():
            # Get uncertainty scores
            uncertainty_scores = [1 - cs for cs in uq_result.data[col]]

            for metric in metrics:
                # Calculate metric score
                if metric == "auprc":
                    score_value = average_precision_score(incorrect_indicators, uncertainty_scores)
                else:  # auroc
                    score_value = roc_auc_score(correct_indicators, uq_result.data[col])
                # Determine category and store score
                if col in Black_Box_Scorers:
                    category = "Black-box"
                elif col in White_Box_Scorers:
                    category = "White-box"
                elif col[:6] == "judge_":
                    category = "Judges"
                elif col in Ensemble:
                    category = "Ensemble"
                method_name = Method_Names.get(col, col.replace("_", " ").title())
                scores[metric][category][method_name] = score_value
    # Remove empty categories
    for metric in metrics:
        empty_keys = [k for k, v in scores[metric].items() if not v]
        for k in empty_keys:
            del scores[metric][k]

    # Create plots
    if len(metrics) == 2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        _plot_single_metric(ax1, scores["auroc"], bar_colors, "AUROC", fontsize, fontname, baseline)
        _plot_single_metric(ax2, scores["auprc"], bar_colors, "AUPRC", fontsize, fontname, baseline)
        fig.suptitle(title.replace("AUROC", "AUROC & AUPRC"), fontsize=fontsize + 2, fontname=fontname)
        plt.tight_layout()
    else:
        _, ax = plt.subplots(figsize=(10, 6))
        metric = metrics[0]
        metric_name = "AUPRC" if metric == "auprc" else "AUROC"
        _plot_single_metric(ax, scores[metric], bar_colors, metric_name, fontsize, fontname, baseline)
        ax.set_title(title.replace("AUROC", metric_name), fontsize=fontsize, fontname=fontname)
    if write_path:
        plt.savefig(f"{write_path}", dpi=300)
    plt.show()
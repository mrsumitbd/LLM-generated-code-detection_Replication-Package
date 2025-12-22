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
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.metrics import roc_auc_score, auc, precision_recall_curve
    
    correct_indicators = np.asarray(correct_indicators)
    
    if scorers_names is None:
        scorers_names = list(uq_result.scores.keys())
    
    # Compute metrics for each scorer
    auroc_scores = {}
    auprc_scores = {}
    
    for scorer_name in scorers_names:
        if scorer_name in uq_result.scores:
            scores = np.asarray(uq_result.scores[scorer_name])
            
            if metric_type in ["auroc", "both"]:
                try:
                    auroc_scores[scorer_name] = roc_auc_score(correct_indicators, scores)
                except:
                    auroc_scores[scorer_name] = 0.5
            
            if metric_type in ["auprc", "both"]:
                try:
                    precision, recall, _ = precision_recall_curve(correct_indicators, scores)
                    auprc_scores[scorer_name] = auc(recall, precision)
                except:
                    auprc_scores[scorer_name] = 0.5
    
    # Sort by scores
    if metric_type == "auroc":
        sorted_items = sorted(auroc_scores.items(), key=lambda x: x[1], reverse=True)
        names = [item[0] for item in sorted_items]
        scores = [item[1] for item in sorted_items]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(names)), scores, color='steelblue', alpha=0.8)
        ax.axhline(y=baseline, color='red', linestyle='--', linewidth=2, label=f'Baseline ({baseline})')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=fontsize, fontname=fontname)
        ax.set_ylabel('AUROC', fontsize=fontsize, fontname=fontname)
        ax.set_ylim([0, 1])
        ax.set_title(title, fontsize=fontsize+2, fontname=fontname)
        ax.legend(fontsize=fontsize)
        ax.grid(axis='y', alpha=0.3)
        
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                   f'{score:.3f}', ha='center', va='bottom', fontsize=fontsize, fontname=fontname)
    
    elif metric_type == "auprc":
        sorted_items = sorted(auprc_scores.items(), key=lambda x: x[1], reverse=True)
        names = [item[0] for item in sorted_items]
        scores = [item[1] for item in sorted_items]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(names)), scores, color='steelblue', alpha=0.8)
        ax.axhline(y=baseline, color='red', linestyle='--', linewidth=2, label=f'Baseline ({baseline})')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=fontsize, fontname=fontname)
        ax.set_ylabel('AUPRC', fontsize=fontsize, fontname=fontname)
        ax.set_ylim([0, 1])
        ax.set_title(title.replace("AUROC", "AUPRC"), fontsize=fontsize+2, fontname=fontname)
        ax.legend(fontsize=fontsize)
        ax.grid(axis='y', alpha=0.3)
        
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                   f'{score:.3f}', ha='center', va='bottom', fontsize=fontsize, fontname=fontname)
    
    elif metric_type == "both":
        sorted_auroc = sorted(auroc_scores.items(), key=lambda x: x[1], reverse=True)
        names = [item[0] for item in sorted_auroc]
        auroc_vals = [auroc_scores[name] for name in names]
        auprc_vals = [auprc_scores[name] for name in names]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        bars1 = ax1.bar(range(len(names)), auroc_vals, color='steelblue', alpha=0.8)
        ax1.axhline(y=baseline, color='red', linestyle='--', linewidth=2, label=f'Baseline ({baseline})')
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=fontsize, fontname=fontname)
        ax1.set_ylabel('AUROC', fontsize=fontsize, fontname=fontname)
        ax1.set_ylim([0, 1])
        ax1.set_title('AUROC', fontsize=fontsize+2, fontname=fontname)
        ax1.legend(fontsize=fontsize)
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, score in zip(bars1, auroc_vals):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                    f'{score:.3f}', ha='center', va='bottom', fontsize=fontsize, fontname=fontname)
        
        bars2 = ax2.bar(range(len(names)), auprc_vals, color='steelblue', alpha=0.8)
        ax2.axhline(y=baseline, color='red', linestyle='--', linewidth=2, label=f'Baseline ({baseline})')
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=fontsize, fontname=fontname)
        ax2.set_ylabel('AUPRC', fontsize=fontsize, fontname=fontname)
        ax2.set_ylim([0, 1])
        ax2.set_title('AUPRC', fontsize=fontsize+2, fontname=fontname)
        ax2.legend(fontsize=fontsize)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, score in zip(bars2, auprc_vals):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                    f'{score:.3f}', ha='center', va='bottom', fontsize=fontsize, fontname=fontname)
        
        fig.suptitle(title, fontsize=fontsize+2, fontname=fontname)
    
    plt.tight_layout()
    
    if write_path is not None:
        plt.savefig(write_path, dpi=300, bbox_inches='tight')
    
    plt.show()
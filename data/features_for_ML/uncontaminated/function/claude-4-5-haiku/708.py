def plot_recall_vs_precision(scores, nodes, node2attacks, labels, out_file):
    """
    Plot the recall vs precision using anomaly scores, node IDs, ground truth labels,
    and a mapping of node IDs to their respective attack numbers.

    This function calculates precision on the x-axis and recall on the y-axis, handles duplicate
    x-values by taking the maximum y-value for each unique x-value, and then plots it with a
    filled area under the curve.
    Ensures that the plot starts at (0, 0).
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Create a list of (score, node_id, label) tuples
    score_node_label = [(scores[i], nodes[i], labels[i]) for i in range(len(scores))]
    
    # Sort by score in descending order
    score_node_label.sort(key=lambda x: x[0], reverse=True)
    
    # Get total number of positive instances (attacks)
    total_attacks = sum(1 for label in labels if label == 1)
    
    if total_attacks == 0:
        return
    
    precisions = []
    recalls = []
    
    tp = 0
    fp = 0
    
    # Iterate through sorted scores
    for score, node_id, label in score_node_label:
        if label == 1:
            tp += 1
        else:
            fp += 1
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / total_attacks if total_attacks > 0 else 0
        
        precisions.append(precision)
        recalls.append(recall)
    
    # Handle duplicate x-values (precision) by taking maximum y-value (recall)
    precision_recall_dict = {}
    for p, r in zip(precisions, recalls):
        if p not in precision_recall_dict:
            precision_recall_dict[p] = r
        else:
            precision_recall_dict[p] = max(precision_recall_dict[p], r)
    
    # Sort by precision
    sorted_precisions = sorted(precision_recall_dict.keys())
    sorted_recalls = [precision_recall_dict[p] for p in sorted_precisions]
    
    # Ensure plot starts at (0, 0)
    if sorted_precisions[0] != 0:
        sorted_precisions.insert(0, 0)
        sorted_recalls.insert(0, 0)
    
    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.fill_between(sorted_precisions, sorted_recalls, alpha=0.3)
    plt.plot(sorted_precisions, sorted_recalls, linewidth=2)
    
    plt.xlabel('Precision', fontsize=12)
    plt.ylabel('Recall', fontsize=12)
    plt.title('Recall vs Precision', fontsize=14)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
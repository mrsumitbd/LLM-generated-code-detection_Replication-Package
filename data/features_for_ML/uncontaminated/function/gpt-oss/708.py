import matplotlib.pyplot as plt
import numpy as np

def plot_recall_vs_precision(scores, nodes, node2attacks, labels, out_file):
    """
    Plot the recall vs precision using anomaly scores, node IDs, ground truth labels,
    and a mapping of node IDs to their respective attack numbers.

    This function calculates precision on the x-axis and recall on the y-axis, handles duplicate
    x-values by taking the maximum y-value for each unique x-value, and then plots it with a
    filled area under the curve.
    Ensures that the plot starts at (0, 0).
    """
    # Determine ground truth for each node
    # If labels is a dict mapping node -> bool/int, use it; otherwise infer from node2attacks
    if isinstance(labels, dict):
        gt = {node: bool(labels.get(node, 0)) for node in nodes}
    else:
        # Assume labels is a list aligned with nodes
        gt = {node: bool(label) for node, label in zip(nodes, labels)}

    # Build list of (score, node, is_attacked)
    data = [(score, node, gt[node]) for score, node in zip(scores, nodes)]
    # Sort by descending score
    data.sort(key=lambda x: x[0], reverse=True)

    total_positives = sum(1 for _, _, attacked in data if attacked)
    if total_positives == 0:
        raise ValueError("No positive instances in the data; cannot compute recall/precision.")

    tp = 0
    fp = 0
    precisions = []
    recalls = []

    for score, node, attacked in data:
        if attacked:
            tp += 1
        else:
            fp += 1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / total_positives
        precisions.append(precision)
        recalls.append(recall)

    # Ensure the curve starts at (0,0)
    precisions = [0.0] + precisions
    recalls = [0.0] + recalls

    # Handle duplicate precision values: keep maximum recall for each precision
    prec_to_rec = {}
    for p, r in zip(precisions, recalls):
        if p in prec_to_rec:
            if r > prec_to_rec[p]:
                prec_to_rec[p] = r
        else:
            prec_to_rec[p] = r

    # Sort by precision ascending
    sorted_items = sorted(prec_to_rec.items())
    sorted_precisions, sorted_recalls = zip(*sorted_items)

    # Plot
    plt.figure(figsize=(6, 6))
    plt.plot(sorted_precisions, sorted_recalls, color='b', lw=2, label='Recall vs Precision')
    plt.fill_between(sorted_precisions, sorted_recalls, step='post', alpha=0.2, color='b')
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.title('Recall vs Precision Curve')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file)
    plt.close()
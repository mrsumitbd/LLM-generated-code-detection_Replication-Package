from collections import defaultdict
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
    # Sort nodes by descending anomaly scores
    sorted_indices = np.argsort(scores)[::-1]
    sorted_nodes = [nodes[i] for i in sorted_indices]
    sorted_labels = [labels[i] for i in sorted_indices]

    # Initialize variables for tracking true positives and recall
    total_positives = np.sum(labels)  # Total number of actual positives
    tp = 0  # True positives
    fp = 0  # False positives

    recalls = [0]  # Start at y=0
    precisions = [0]  # Start at x=0

    # Count true positives and calculate precision and recall at each threshold
    for i, node in enumerate(sorted_nodes):
        # Update tp and fp based on the current label
        if sorted_labels[i] == 1:
            tp += 1
        else:
            fp += 1

        # Calculate precision and recall
        precision = tp / (tp + fp)
        recall = tp / total_positives

        precisions.append(precision)
        recalls.append(recall)

    # Use max recall for each unique precision
    precision_to_recall = defaultdict(list)
    for precision, recall in zip(precisions, recalls):
        precision_to_recall[precision].append(recall)

    unique_precisions = []
    max_recalls = []
    for precision, recall_list in sorted(precision_to_recall.items()):
        unique_precisions.append(precision)
        max_recalls.append(np.max(recall_list))

    # Calculate area under the curve for recall vs precision
    area_under_curve = np.trapz(max_recalls, unique_precisions) / 100

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(
        unique_precisions,
        max_recalls,
        color="b",
        label=f"Area under curve = {area_under_curve:.2f}",
    )
    plt.fill_between(unique_precisions, max_recalls, color="blue", alpha=0.2)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("Recall vs Precision")
    plt.legend(loc="lower left")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.savefig(out_file)
    return area_under_curve
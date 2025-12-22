import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

def plot_recall_vs_precision(scores, nodes, node2attacks, labels, out_file):
    """
    Plot the recall vs precision using anomaly scores, node IDs, ground truth labels,
    and a mapping of node IDs to their respective attack numbers.

    This function calculates precision on the x-axis and recall on the y-axis, handles duplicate
    x-values by taking the maximum y-value for each unique x-value, and then plots it with a
    filled area under the curve.
    Ensures that the plot starts at (0, 0).
    """
    precision, recall, _ = precision_recall_curve(labels, scores)

    # Handle duplicate x-values by taking the maximum y-value for each unique x-value
    unique_precision = np.unique(precision)
    unique_recall = [np.max(recall[precision == p]) for p in unique_precision]

    # Ensure the plot starts at (0, 0)
    unique_precision = np.concatenate([[0], unique_precision])
    unique_recall = np.concatenate([[0], unique_recall])

    # Plot the recall vs precision curve with filled area under the curve
    plt.figure(figsize=(8, 6))
    plt.plot(unique_precision, unique_recall, color='b')
    plt.fill_between(unique_precision, unique_recall, color='b', alpha=0.2)
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.title('Recall vs Precision')
    plt.savefig(out_file)
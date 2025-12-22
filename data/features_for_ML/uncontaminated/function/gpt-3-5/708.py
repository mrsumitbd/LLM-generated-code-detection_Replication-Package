def plot_recall_vs_precision(scores, nodes, node2attacks, labels, out_file):
    import matplotlib.pyplot as plt
    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import auc

    precision, recall, _ = precision_recall_curve(labels, scores)
    area = auc(recall, precision)

    plt.figure()
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve: AUC={0:0.2f}'.format(area))
    plt.savefig(out_file)
    plt.close()
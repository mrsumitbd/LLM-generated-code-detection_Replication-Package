def evaluate(pred, target, metrics, id2type):
    results = {}
    for metric in metrics:
        if metric == 'accuracy':
            correct = 0
            total = 0
            for p, t in zip(pred, target):
                if p == t:
                    correct += 1
                total += 1
            results['accuracy'] = correct / total
        elif metric == 'precision':
            tp = 0
            fp = 0
            for p, t in zip(pred, target):
                if p == t and p == id2type['positive']:
                    tp += 1
                elif p != t and p == id2type['positive']:
                    fp += 1
            results['precision'] = tp / (tp + fp) if tp + fp > 0 else 0
        elif metric == 'recall':
            tp = 0
            fn = 0
            for p, t in zip(pred, target):
                if p == t and p == id2type['positive']:
                    tp += 1
                elif p != t and t == id2type['positive']:
                    fn += 1
            results['recall'] = tp / (tp + fn) if tp + fn > 0 else 0
    return results
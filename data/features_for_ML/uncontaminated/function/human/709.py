def print_metrics(metrics: dict[str, dict[str, float]]) -> None:
    """Print evaluation metrics in a readable format.

    :param metrics: A dictionary containing the evaluation metrics.
    :return: None
    """
    print("\nEvaluation Results:")
    print("\nHallucination Detection (Class 1):")
    print(f"  Precision: {metrics['hallucinated']['precision']:.4f}")
    print(f"  Recall: {metrics['hallucinated']['recall']:.4f}")
    print(f"  F1: {metrics['hallucinated']['f1']:.4f}")

    print("\nSupported Content (Class 0):")
    print(f"  Precision: {metrics['supported']['precision']:.4f}")
    print(f"  Recall: {metrics['supported']['recall']:.4f}")
    print(f"  F1: {metrics['supported']['f1']:.4f}")

    print(f"\nAUROC: {metrics['auroc']:.4f}")
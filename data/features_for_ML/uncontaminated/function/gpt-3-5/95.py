def compute_au_alignment_metrics(
    au_csv_path: Optional[str],
    peak_frame_index: Optional[int],
    peak_frame_au_text: Optional[str],
    presence_threshold: float = 0.8,
    peak_au_intensities: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    
    def compute_precision_recall_f1(true_positives, false_positives, false_negatives):
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return {'precision': precision, 'recall': recall, 'f1': f1}
    
    return compute_precision_recall_f1(0, 0, 0)
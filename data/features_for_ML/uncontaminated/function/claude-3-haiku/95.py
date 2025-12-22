import csv
from typing import Optional, Dict
from collections import defaultdict

def compute_au_alignment_metrics(
    au_csv_path: Optional[str],
    peak_frame_index: Optional[int],
    peak_frame_au_text: Optional[str],
    presence_threshold: float = 0.8,
    peak_frame_au_intensities: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Compare AUs mentioned in text to actual OpenFace AUs around the peak frame.

    Returns precision/recall/f1 on AU presence.
    """
    if au_csv_path is None or peak_frame_index is None or peak_frame_au_text is None:
        return {}

    au_presence = defaultdict(bool)
    au_intensities = defaultdict(float)

    with open(au_csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            frame_index = int(row['frame'])
            if abs(frame_index - peak_frame_index) <= 1:
                for au, intensity in peak_frame_au_intensities.items():
                    au_presence[au] = intensity >= presence_threshold
                    au_intensities[au] = intensity

    text_aus = set(peak_frame_au_text.split(','))
    actual_aus = set(au_presence.keys())

    true_positives = len(text_aus.intersection(actual_aus))
    false_positives = len(text_aus - actual_aus)
    false_negatives = len(actual_aus - text_aus)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'au_presence': au_presence,
        'au_intensities': au_intensities,
    }
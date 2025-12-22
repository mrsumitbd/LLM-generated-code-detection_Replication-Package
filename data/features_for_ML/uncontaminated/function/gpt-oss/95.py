import re
from typing import Dict, Optional

import pandas as pd


def compute_au_alignment_metrics(
    au_csv_path: Optional[str],
    peak_frame_index: Optional[int],
    peak_frame_au_text: Optional[str],
    presence_threshold: float = 0.8,
    peak_au_intensities: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Compare AUs mentioned in text to actual OpenFace AUs around the peak frame.

    Returns precision/recall/f1 on AU presence.
    """
    # Helper to extract AU names from text
    def _extract_aus(text: str) -> set:
        if not text:
            return set()
        return set(re.findall(r"AU\d{2}", text))

    # Get AU intensities for the peak frame
    if peak_au_intensities is None:
        if au_csv_path is None or peak_frame_index is None:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        try:
            df = pd.read_csv(au_csv_path)
        except Exception:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        if peak_frame_index < 0 or peak_frame_index >= len(df):
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        # Assume columns are AU names
        row = df.iloc[peak_frame_index]
        peak_au_intensities = {col: float(row[col]) for col in df.columns if col.startswith("AU")}
    else:
        # Ensure keys are AU names
        peak_au_intensities = {k: float(v) for k, v in peak_au_intensities.items()}

    # Determine presence of each AU in the peak frame
    actual_present = {au for au, val in peak_au_intensities.items() if val >= presence_threshold}

    # Extract AUs from the text
    text_aus = _extract_aus(peak_frame_au_text)

    # Compute TP, FP, FN
    tp = len(actual_present & text_aus)
    fp = len(text_aus - actual_present)
    fn = len(actual_present - text_aus)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {"precision": precision, "recall": recall, "f1": f1}
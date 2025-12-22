from typing import Dict, Optional, Tuple
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
    results: Dict[str, float] = {
        "au_pr": 0.0,
        "au_re": 0.0,
        "au_f1": 0.0,
    }
    presence: Dict[str, int] = {}
    if peak_au_intensities is not None and isinstance(peak_au_intensities, dict) and peak_au_intensities:
        # Build presence directly from provided intensities
        presence = {
            k if k.endswith("_r") else f"{k}_r": int(float(v) >= presence_threshold)
            for k, v in peak_au_intensities.items()
            if str(k).upper().startswith("AU")
        }
        # If after filtering we got no AUs, return zeros
        if not presence:
            return results
    elif au_csv_path and peak_frame_index is not None:
        try:
            df = pd.read_csv(au_csv_path)
        except Exception:
            return results
        if df.empty:
            return results
        idx = max(0, min(int(peak_frame_index), len(df) - 1))
        row = df.iloc[idx]
        presence = _presence_from_intensity_row(row, presence_threshold)
        # If no valid AU columns found in CSV, return zeros
        if not presence:
            return results
    else:
        return results
    mentioned = _extract_mentioned_aus(peak_frame_au_text or "")

    # Build sets
    predicted_set = {k for k, v in presence.items() if v == 1}
    mentioned_set = set(mentioned.keys())
    
    # If both sets are empty, return zeros (no data to evaluate)
    if not predicted_set and not mentioned_set:
        return results

    tp = len(predicted_set & mentioned_set)
    fp = len(mentioned_set - predicted_set)
    fn = len(predicted_set - mentioned_set)

    p, r, f1 = _precision_recall_f1(tp, fp, fn)
    results.update({"au_pr": p, "au_re": r, "au_f1": f1})
    return results
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
    # Initialize default metrics
    default_metrics = {
        "au_precision": 0.0,
        "au_recall": 0.0,
        "au_f1": 0.0,
    }
    
    # Validate inputs
    if not peak_frame_au_text or peak_frame_index is None:
        return default_metrics
    
    # Extract AUs mentioned in text
    text_aus = set()
    if peak_frame_au_text:
        # Extract AU numbers from text (e.g., "AU01", "AU 01", "AU1", etc.)
        import re
        au_pattern = r'AU\s*(\d+)'
        matches = re.findall(au_pattern, peak_frame_au_text, re.IGNORECASE)
        for match in matches:
            au_num = int(match)
            text_aus.add(au_num)
    
    if not text_aus:
        return default_metrics
    
    # Get actual AUs from CSV or provided intensities
    actual_aus = set()
    
    if peak_au_intensities:
        # Use provided AU intensities
        for au_name, intensity in peak_au_intensities.items():
            if intensity >= presence_threshold:
                # Extract AU number from name (e.g., "AU01" -> 1)
                import re
                match = re.search(r'(\d+)', au_name)
                if match:
                    au_num = int(match.group(1))
                    actual_aus.add(au_num)
    elif au_csv_path and peak_frame_index is not None:
        # Read from CSV file
        try:
            import pandas as pd
            df = pd.read_csv(au_csv_path)
            
            # Find the row corresponding to peak_frame_index
            if peak_frame_index < len(df):
                row = df.iloc[peak_frame_index]
                
                # Extract AU columns (typically named like " AU01_r", " AU02_r", etc.)
                for col in df.columns:
                    if 'AU' in col and '_r' in col:
                        try:
                            intensity = float(row[col])
                            if intensity >= presence_threshold:
                                # Extract AU number
                                import re
                                match = re.search(r'AU(\d+)', col)
                                if match:
                                    au_num = int(match.group(1))
                                    actual_aus.add(au_num)
                        except (ValueError, TypeError):
                            pass
        except Exception:
            return default_metrics
    
    if not actual_aus:
        return default_metrics
    
    # Calculate precision, recall, and F1
    true_positives = len(text_aus & actual_aus)
    false_positives = len(text_aus - actual_aus)
    false_negatives = len(actual_aus - text_aus)
    
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )
    
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0.0
    )
    
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    
    return {
        "au_precision": precision,
        "au_recall": recall,
        "au_f1": f1,
    }
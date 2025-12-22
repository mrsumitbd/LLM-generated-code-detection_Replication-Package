def filter_solutions(dataset):
    """
    Return a new list containing only the items that are marked as correct.
    The function is tolerant to different data structures:
    - If the dataset is a list of dictionaries, it looks for keys
      'is_correct', 'label', or 'correct' to determine correctness.
    - If the dataset is a list of non-dict items, they are kept as-is.
    - If the dataset is not a list, it is returned unchanged.
    """
    if not isinstance(dataset, list):
        return dataset

    filtered = []
    for item in dataset:
        if isinstance(item, dict):
            # Prefer explicit boolean flag
            if item.get("is_correct") is True:
                filtered.append(item)
                continue
            # Fall back to string labels
            label = item.get("label")
            if isinstance(label, str) and label.lower() == "correct":
                filtered.append(item)
                continue
            # Another possible flag
            if item.get("correct") is True:
                filtered.append(item)
                continue
            # If none of the flags are present, assume correct
            if "is_correct" not in item and "label" not in item and "correct" not in item:
                filtered.append(item)
        else:
            # Non-dict items are kept
            filtered.append(item)

    return filtered
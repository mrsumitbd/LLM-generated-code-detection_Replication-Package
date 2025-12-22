def filter_solutions(dataset):
    # First filter out incorrect responses.
    filtered = []
    for item in dataset:
        if isinstance(item, dict) and 'is_correct' in item:
            if item.get('is_correct', False):
                filtered.append(item)
        elif isinstance(item, dict) and 'correct' in item:
            if item.get('correct', False):
                filtered.append(item)
        elif isinstance(item, dict) and 'solution' in item:
            filtered.append(item)
        elif isinstance(item, (list, tuple)) and len(item) > 0:
            if isinstance(item[-1], bool) and item[-1]:
                filtered.append(item)
            elif isinstance(item[-1], bool) and not item[-1]:
                continue
            else:
                filtered.append(item)
        else:
            filtered.append(item)
    return filtered
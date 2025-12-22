def preprocess(examples):
    """
    Generic preprocessing routine for a collection of examples.
    Handles lists of strings or dictionaries containing string values.
    Strips whitespace and lower‑cases all string entries.
    """
    processed = []

    for ex in examples:
        # If the example is a dictionary, process each string field
        if isinstance(ex, dict):
            new_ex = {}
            for key, value in ex.items():
                if isinstance(value, str):
                    new_ex[key] = value.strip().lower()
                else:
                    new_ex[key] = value
            processed.append(new_ex)

        # If the example is a plain string, clean it directly
        elif isinstance(ex, str):
            processed.append(ex.strip().lower())

        # For any other type, keep it unchanged
        else:
            processed.append(ex)

    return processed
import os

def load_expected_answer(label_path):
    """
    Load the expected answer from label.txt file.
    Returns a dictionary with the expected values.
    """
    label_file = os.path.join(label_path, "label.txt")
    if not os.path.isfile(label_file):
        raise FileNotFoundError(f"Expected label file not found: {label_file}")

    expected = {}
    with open(label_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Try colon first, then equals
            if ":" in line:
                key, val = line.split(":", 1)
            elif "=" in line:
                key, val = line.split("=", 1)
            else:
                # If no separator, treat whole line as key with empty value
                key, val = line, ""
            key = key.strip()
            val = val.strip()
            expected[key] = val
    return expected
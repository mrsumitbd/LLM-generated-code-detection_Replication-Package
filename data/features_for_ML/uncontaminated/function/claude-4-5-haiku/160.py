import anthropic
import json
import os


def load_expected_answer(label_path):
    """
    Load the expected answer from label.txt file.
    Returns a dictionary with the expected values.
    """
    if not os.path.exists(label_path):
        raise FileNotFoundError(f"Label file not found at {label_path}")
    
    with open(label_path, 'r') as f:
        content = f.read().strip()
    
    try:
        expected_answer = json.loads(content)
    except json.JSONDecodeError:
        expected_answer = {"raw_content": content}
    
    return expected_answer
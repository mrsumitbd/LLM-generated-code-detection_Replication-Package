def load_expected_answer(label_path):
    """
    Load the expected answer from label.txt file.
    Returns a dictionary with the expected values.
    """
    expected_answer = {}
    with open(label_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            expected_answer[key] = value
    return expected_answer
def load_expected_answer(label_path):
    expected_answer = {}
    with open(label_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            expected_answer[key.strip()] = value.strip()
    return expected_answer
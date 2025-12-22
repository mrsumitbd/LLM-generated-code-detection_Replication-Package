def preprocess(examples):
    preprocessed_examples = []
    for example in examples:
        text = example.lower()
        text = ''.join(char for char in text if char.isalnum() or char == ' ')
        words = text.split()
        preprocessed_example = ' '.join(words)
        preprocessed_examples.append(preprocessed_example)
    return preprocessed_examples
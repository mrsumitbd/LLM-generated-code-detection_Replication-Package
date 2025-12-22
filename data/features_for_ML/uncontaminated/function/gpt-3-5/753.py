def preprocess(examples):
    preprocessed_examples = []
    for example in examples:
        preprocessed_example = example.upper()
        preprocessed_examples.append(preprocessed_example)
    return preprocessed_examples
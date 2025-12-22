def preprocess(sample, is_cot=False):
    if is_cot:
        return sample.upper()
    else:
        return sample.lower()
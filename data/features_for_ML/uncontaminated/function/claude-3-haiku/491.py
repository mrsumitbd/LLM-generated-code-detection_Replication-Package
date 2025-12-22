import numpy as np

def preprocess(sample, is_cot=False):
    if is_cot:
        sample = np.log1p(sample)
    else:
        sample = np.sqrt(sample)
    
    sample = (sample - sample.mean()) / sample.std()
    
    return sample
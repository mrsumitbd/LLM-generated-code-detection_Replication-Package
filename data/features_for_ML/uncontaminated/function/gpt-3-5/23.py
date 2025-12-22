import numpy as np
import librosa

def audio_compute_mfcc(data, config: DataConfig):
    mfcc = librosa.feature.mfcc(y=data, sr=config.sample_rate, n_mfcc=config.n_mfcc, hop_length=config.hop_length)
    return mfcc
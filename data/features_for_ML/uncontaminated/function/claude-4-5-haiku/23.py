def audio_compute_mfcc(data, config: DataConfig):
    """ Extract mfcc
    """
    import librosa
    import numpy as np
    
    # Load audio file
    if isinstance(data, str):
        y, sr = librosa.load(data, sr=config.sample_rate)
    else:
        y = data
        sr = config.sample_rate
    
    # Compute MFCC
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=config.n_mfcc,
        n_fft=config.n_fft,
        hop_length=config.hop_length,
        n_mels=config.n_mels
    )
    
    # Transpose to get shape (time_steps, n_mfcc)
    mfcc = mfcc.T
    
    return mfcc
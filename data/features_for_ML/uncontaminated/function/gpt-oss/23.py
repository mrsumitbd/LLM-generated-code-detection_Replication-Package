import numpy as np
import librosa

def audio_compute_mfcc(data, config: 'DataConfig'):
    """
    Extract MFCC features from an audio signal.

    Parameters
    ----------
    data : np.ndarray
        Audio time series. If the input is multi‑channel, the channels are averaged.
    config : DataConfig
        Configuration object containing audio parameters. Expected attributes:
        - sample_rate : int, sampling rate of the audio.
        - n_mfcc : int, number of MFCC coefficients to return.
        - hop_length : int, number of samples between successive frames.
        - n_fft : int, FFT window size.

    Returns
    -------
    np.ndarray
        2‑D array of shape (n_mfcc, t) where t is the number of frames.
    """
    # Ensure data is a 1‑D array (mono). If stereo, average channels.
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Pull parameters from config with sensible defaults
    sr = getattr(config, 'sample_rate', 22050)
    n_mfcc = getattr(config, 'n_mfcc', 20)
    hop_length = getattr(config, 'hop_length', 512)
    n_fft = getattr(config, 'n_fft', 2048)

    # Compute MFCCs
    mfcc = librosa.feature.mfcc(
        y=data,
        sr=sr,
        n_mfcc=n_mfcc,
        hop_length=hop_length,
        n_fft=n_fft
    )

    return mfcc
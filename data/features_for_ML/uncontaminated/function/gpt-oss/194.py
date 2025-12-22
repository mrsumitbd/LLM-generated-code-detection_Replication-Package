import numpy as np
from scipy.signal import butter, lfilter

def process_audio(audio_data=decrypted):
    """
    Process raw audio data by normalizing amplitude and applying a low‑pass filter.
    Parameters
    ----------
    audio_data : array_like or None
        Raw audio samples. If None, the function returns None.
    Returns
    -------
    processed : np.ndarray or None
        The filtered audio samples, normalized to the range [-1, 1].
    """
    # If no data provided, return None
    if audio_data is None:
        return None

    # Convert input to a NumPy array
    try:
        samples = np.asarray(audio_data, dtype=float)
    except Exception:
        return None

    # Flatten in case of multi‑dimensional input
    samples = samples.flatten()

    # Avoid division by zero
    max_val = np.max(np.abs(samples))
    if max_val == 0:
        return samples

    # Normalize to [-1, 1]
    samples = samples / max_val

    # Design a low‑pass Butterworth filter (cutoff 4000 Hz, sample rate 44100 Hz)
    # Adjust if sample rate differs; here we assume 44.1 kHz
    fs = 44100.0
    cutoff = 4000.0
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(N=4, Wn=normal_cutoff, btype='low', analog=False)

    # Apply the filter
    filtered = lfilter(b, a, samples)

    return filtered
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import hamming

def audio_compute_mfcc(data, config: DataConfig):
    """Extract mfcc"""
    # Compute the Short-Time Fourier Transform (STFT)
    window = hamming(config.frame_size, sym=False)
    frames = np.lib.stride_tricks.as_strided(
        data,
        shape=(data.shape[0] - config.frame_size + 1, config.frame_size),
        strides=(data.itemsize, data.itemsize)
    )
    stft = np.fft.rfft(frames * window[None, :], axis=1)

    # Compute the Mel-Frequency Cepstral Coefficients (MFCC)
    mel_filters = create_mel_filters(config.sample_rate, config.frame_size, config.num_mel_filters, config.min_freq, config.max_freq)
    mel_spectrogram = np.dot(np.abs(stft) ** 2, mel_filters.T)
    mfcc = dct(np.log(mel_spectrogram + 1e-8), type=2, axis=1, norm='ortho')[:, :config.num_mfcc]

    return mfcc

def create_mel_filters(sample_rate, frame_size, num_mel_filters, min_freq, max_freq):
    """Create Mel-frequency filters"""
    mel_min = 2595 * np.log10(1 + min_freq / 700)
    mel_max = 2595 * np.log10(1 + max_freq / 700)
    mel_points = np.linspace(mel_min, mel_max, num_mel_filters + 2)
    bin_frequencies = np.linspace(0, sample_rate / 2, frame_size // 2 + 1)
    mel_filters = []
    for i in range(1, num_mel_filters + 1):
        left = 700 * (10 ** ((mel_points[i - 1]) / 2595) - 1)
        center = 700 * (10 ** ((mel_points[i]) / 2595) - 1)
        right = 700 * (10 ** ((mel_points[i + 1]) / 2595) - 1)

        filt_vals = (np.abs(bin_frequencies - left) / (center - left),
                    np.abs(bin_frequencies - right) / (right - center))
        filter_shape = np.minimum(filt_vals[0], filt_vals[1])
        mel_filters.append(filter_shape)

    return np.array(mel_filters)

def dct(x, type=2, axis=-1, norm='ortho'):
    """Discrete Cosine Transform"""
    x = np.asarray(x)
    if type == 2:
        # return scipy.fft.dct(x, norm=norm, axis=axis)
        return scipy.fft.dct(x, type=2, norm=norm, axis=axis)
    else:
        raise ValueError("Only DCT type 2 is currently supported.")
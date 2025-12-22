import torch
import torchaudio
import numpy as np
from typing import Union, Optional

def log_mel_spectrogram(
    audio: Union[str, np.ndarray, torch.Tensor],
    n_mels: int = 80,
    padding: int = 0,
    device: Optional[Union[str, torch.device]] = None,
):
    """
    Compute the log-Mel spectrogram of

    Parameters
    ----------
    audio: Union[str, np.ndarray, torch.Tensor], shape = (*)
        The path to audio or either a NumPy array or Tensor containing the audio waveform in 16 kHz

    n_mels: int
        The number of Mel-frequency filters, only 80 and 128 are supported

    padding: int
        Number of zero samples to pad to the right

    device: Optional[Union[str, torch.device]]
        If given, the audio tensor is moved to this device before STFT

    Returns
    -------
    torch.Tensor, shape = (n_mels, n_frames)
        A Tensor that contains the Mel spectrogram
    """
    if isinstance(audio, str):
        waveform, _ = torchaudio.load(audio)
    elif isinstance(audio, np.ndarray):
        waveform = torch.from_numpy(audio)
    elif isinstance(audio, torch.Tensor):
        waveform = audio
    else:
        raise ValueError("audio must be a string, numpy array, or torch tensor")

    if device is not None:
        waveform = waveform.to(device)

    # Compute the STFT
    stft = torch.stft(waveform, n_fft=2048, hop_length=512, window=torch.hann_window(2048), return_complex=True)

    # Compute the Mel spectrogram
    mel_spectrogram = torchaudio.functional.melscale_fbank(stft, sample_rate=16000, n_mels=n_mels)

    # Take the log of the Mel spectrogram
    log_mel_spectrogram = torch.log(mel_spectrogram + 1e-8)

    # Pad the log Mel spectrogram if necessary
    if padding > 0:
        log_mel_spectrogram = torch.nn.functional.pad(log_mel_spectrogram, (0, padding), mode='constant', value=0)

    return log_mel_spectrogram
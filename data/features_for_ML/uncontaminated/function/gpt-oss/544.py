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
    # Validate n_mels
    if n_mels not in (80, 128):
        raise ValueError("n_mels must be either 80 or 128")

    # Load audio if path
    if isinstance(audio, str):
        waveform, sr = torchaudio.load(audio)
        if sr != 16000:
            waveform = torchaudio.functional.resample(waveform, sr, 16000)
    elif isinstance(audio, np.ndarray):
        waveform = torch.from_numpy(audio).float()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        if device is not None:
            waveform = waveform.to(device)
    elif isinstance(audio, torch.Tensor):
        waveform = audio.float()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        if device is not None:
            waveform = waveform.to(device)
    else:
        raise TypeError("audio must be a path, numpy array, or torch tensor")

    # Pad to the right
    if padding > 0:
        waveform = torch.nn.functional.pad(waveform, (0, padding))

    # STFT parameters
    n_fft = 400          # 25 ms window at 16 kHz
    hop_length = 160     # 10 ms hop
    win_length = 400

    # Mel spectrogram transform
    mel_spec_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=16000,
        n_fft=n_fft,
        win_length=win_length,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0,
        center=True,
        pad_mode="reflect",
    ).to(device if device is not None else waveform.device)

    # Compute mel spectrogram
    mel_spec = mel_spec_transform(waveform)  # shape: (1, n_mels, n_frames)

    # Log scaling
    log_mel = torch.log10(mel_spec + 1e-10).squeeze(0)  # shape: (n_mels, n_frames)

    return log_mel
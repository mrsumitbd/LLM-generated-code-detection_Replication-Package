from typing import Union, Optional
import numpy as np
import torch
from torchaudio.transforms import MelSpectrogram

def log_mel_spectrogram(
    audio: Union[str, np.ndarray, torch.Tensor],
    n_mels: int = 80,
    padding: int = 0,
    device: Optional[Union[str, torch.device]] = None,
):
    if n_mels not in [80, 128]:
        raise ValueError("Only 80 and 128 Mel-frequency filters are supported")

    if isinstance(audio, str):
        audio, _ = torchaudio.load(audio, normalize=True)

    if isinstance(audio, np.ndarray):
        audio = torch.from_numpy(audio).float()

    if device is not None:
        audio = audio.to(device)

    mel_spectrogram = MelSpectrogram(sample_rate=16000, n_mels=n_mels)(audio.unsqueeze(0))
    mel_spectrogram = mel_spectrogram.squeeze(0).log1p()

    return mel_spectrogram
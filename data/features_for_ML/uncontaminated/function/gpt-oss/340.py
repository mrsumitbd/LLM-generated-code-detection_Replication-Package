import torch
import torchaudio
import os

# Default target sample rate (you can adjust if needed)
TARGET_SAMPLE_RATE = 16000

def prepare_sample_waveforms(
    audio_paths,
    cuda_enabled=True,
    sr=TARGET_SAMPLE_RATE,
    max_length_seconds=10
):
    """
    Load a list of audio files, resample them to the target sample rate,
    truncate or pad them to a fixed length, and return a single tensor
    containing all waveforms.

    Parameters
    ----------
    audio_paths : list[str]
        List of file paths to audio files.
    cuda_enabled : bool, optional
        If True and CUDA is available, move the resulting tensor to GPU.
    sr : int, optional
        Target sample rate for all waveforms.
    max_length_seconds : int or float, optional
        Desired length of each waveform in seconds. Waveforms longer than
        this will be truncated; shorter ones will be zero‑padded.

    Returns
    -------
    torch.Tensor
        Tensor of shape (N, C, L) where N is the number of audio files,
        C is the number of channels (1 for mono, 2 for stereo, etc.),
        and L is the number of samples (sr * max_length_seconds).
    """
    device = torch.device("cuda" if cuda_enabled and torch.cuda.is_available() else "cpu")
    target_len = int(sr * max_length_seconds)

    waveforms = []

    for path in audio_paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Audio file not found: {path}")

        # Load audio
        waveform, orig_sr = torchaudio.load(path)  # shape: (C, L)
        waveform = waveform.to(torch.float32)

        # Resample if needed
        if orig_sr != sr:
            resampler = torchaudio.transforms.Resample(orig_sr, sr)
            waveform = resampler(waveform)

        # Truncate or pad to target length
        cur_len = waveform.shape[1]
        if cur_len > target_len:
            waveform = waveform[:, :target_len]
        elif cur_len < target_len:
            pad_amount = target_len - cur_len
            waveform = torch.nn.functional.pad(waveform, (0, pad_amount))

        waveforms.append(waveform)

    # Stack into a single tensor
    batch = torch.stack(waveforms, dim=0).to(device)
    return batch
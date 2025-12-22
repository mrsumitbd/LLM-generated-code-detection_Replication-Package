import os
import numpy as np
import librosa
import torch

def prepare_sample_waveforms(audio_paths, cuda_enabled=True, sr=16000, max_length_seconds=10):
    waveforms = []
    for audio_path in audio_paths:
        waveform, _ = librosa.load(audio_path, sr=sr, mono=True)
        if len(waveform) > sr * max_length_seconds:
            waveform = waveform[:sr * max_length_seconds]
        waveforms.append(waveform)

    waveforms = np.stack(waveforms, axis=0)
    waveforms = torch.from_numpy(waveforms).float()
    if cuda_enabled:
        waveforms = waveforms.cuda()
    return waveforms
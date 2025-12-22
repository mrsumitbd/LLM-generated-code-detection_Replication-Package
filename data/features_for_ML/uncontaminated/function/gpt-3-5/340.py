import torch
import torchaudio

def prepare_sample_waveforms(audio_paths, cuda_enabled=True, sr=TARGET_SAMPLE_RATE, max_length_seconds=10):
    waveforms = []
    for audio_path in audio_paths:
        waveform, _ = torchaudio.load(audio_path, normalize=True)
        if waveform.size(1) > sr * max_length_seconds:
            waveform = waveform[:, :sr * max_length_seconds]
        if cuda_enabled:
            waveform = waveform.cuda()
        waveforms.append(waveform)
    return waveforms
import resampy
import soundfile as sf
import torch

def prepare_sample_waveforms(audio_paths, cuda_enabled=True, sr=TARGET_SAMPLE_RATE, max_length_seconds=10):
    batch_len = sr  # minimum length of audio
    audios = []
    for audio_path in audio_paths:
        audio, loaded_sr = sf.read(audio_path)
        if len(audio.shape) == 2:
            audio = audio[:, 0]
        audio = audio[: loaded_sr * 10]
        audio = resampy.resample(audio, loaded_sr, sr)
        audio = torch.from_numpy(audio)

        if len(audio) < sr * max_length_seconds:
            pad_size = sr * max_length_seconds - len(audio)
            audio = torch.nn.functional.pad(audio, (0, pad_size))
        audio = torch.clamp(audio, -1.0, 1.0)
        if len(audio) > batch_len:
            batch_len = len(audio)
        audios.append(audio)
    padding_mask = torch.zeros((len(audios), batch_len), dtype=torch.bool)
    for i in range(len(audios)):
        if len(audios[i]) < batch_len:
            pad_len = batch_len - len(audios[i])
            sil = torch.zeros(pad_len, dtype=torch.float32)
            audios[i] = torch.cat((audios[i], sil), dim=0)
            padding_mask[i, len(audios[i]) :] = True
    audios = torch.stack(audios, dim=0)

    samples = {
        "raw_wav": audios,
        "padding_mask": padding_mask,
        "audio_chunk_sizes": [len(audio_paths)],
    }
    if cuda_enabled:
        samples = move_to_device(samples, "cuda")

    return samples
import torchaudio
from touchnet.data import DataConfig

def audio_resample(data, config: DataConfig):
    """ Resample data.
        Inplace operation.
    """
    for sample in data:
        assert 'sample_rate' in sample
        assert 'waveform' in sample
        sample_rate = sample['sample_rate']
        waveform = sample['waveform']
        if sample_rate != config.audio_resample_rate:
            sample['sample_rate'] = config.audio_resample_rate
            sample['waveform'] = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=config.audio_resample_rate)(waveform)
        yield sample
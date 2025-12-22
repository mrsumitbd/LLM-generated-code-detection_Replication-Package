import torchaudio.compliance.kaldi as kaldi
from touchnet.data import DataConfig

def audio_compute_mfcc(data, config: DataConfig):
    """ Extract mfcc
    """
    for sample in data:
        assert 'sample_rate' in sample
        assert 'waveform' in sample
        sample_rate = sample['sample_rate']
        waveform = sample['waveform']
        waveform = waveform * (1 << 15)
        mat = kaldi.mfcc(waveform,
                         num_mel_bins=config.audiofeat_num_mel_bins,
                         frame_length=config.audiofeat_frame_length,
                         frame_shift=config.audiofeat_frame_shift,
                         dither=config.audiofeat_dither,
                         num_ceps=config.audiofeat_num_ceps,
                         high_freq=config.audiofeat_high_freq,
                         low_freq=config.audiofeat_low_freq,
                         sample_frequency=sample_rate)
        sample['audiofeat'] = mat
        yield sample
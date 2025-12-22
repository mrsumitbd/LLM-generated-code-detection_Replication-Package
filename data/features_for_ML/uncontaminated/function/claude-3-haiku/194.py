def process_audio(audio_data=decrypted):
    import numpy as np
    from scipy.io.wavfile import write

    # Normalize the audio data
    audio_data = audio_data / np.max(np.abs(audio_data))

    # Apply any desired audio processing here
    # For example, you can apply a low-pass filter
    filtered_audio = apply_low_pass_filter(audio_data)

    # Write the processed audio to a WAV file
    write('processed_audio.wav', 44100, filtered_audio.astype(np.int16))
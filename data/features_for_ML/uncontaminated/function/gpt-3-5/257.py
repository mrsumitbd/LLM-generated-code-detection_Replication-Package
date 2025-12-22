def convert_to_audio(multiframe, count):
    audio = []
    for i in range(count):
        audio.extend(multiframe)
    return audio
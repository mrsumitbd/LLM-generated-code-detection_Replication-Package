def stream_output(stream, prefix):
    for line in stream:
        print(prefix + line, end='')
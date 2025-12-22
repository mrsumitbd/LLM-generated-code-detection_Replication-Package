def stream_output(stream, prefix):
    while True:
        try:
            line = stream.readline().strip()
            if line:
                print(f"{prefix} {line}")
        except Exception as e:
            print(f"Error: {e}")
            break
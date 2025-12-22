def read_stream(stream, q):
            try:
                while True:
                    line = stream.readline()
                    if not line:  # EOF
                        break
                    q.put(line.rstrip("\n\r"))
            except Exception:
                # Signal error/EOF
                q.put(None)
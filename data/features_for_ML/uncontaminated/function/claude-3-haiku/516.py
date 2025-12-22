def read_stream(stream, q):
    try:
        while True:
            data = stream.read(1024)
            if not data:
                break
            q.put(data)
    except Exception as e:
        q.put(e)
    finally:
        q.put(None)
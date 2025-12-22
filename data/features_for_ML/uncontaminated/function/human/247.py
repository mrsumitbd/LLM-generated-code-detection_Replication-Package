def stream_output(stream, prefix):
        try:
            while not shutdown_event.is_set():
                line = stream.readline()
                if not line:  # End of stream
                    break
                if line.strip():  # Only log non-empty lines
                    message = f"{prefix}: {line.strip()}"
                    log_message(message)
        except Exception as e:
            log_message(f"Python: Error reading from {prefix}: {e}")
        finally:
            try:
                stream.close()
            except:
                pass
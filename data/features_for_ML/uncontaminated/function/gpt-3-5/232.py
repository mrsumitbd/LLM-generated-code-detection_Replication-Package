import signal

def signal_handler(sig, frame):
    print(f"Signal {sig} received. Exiting...")
    exit(0)
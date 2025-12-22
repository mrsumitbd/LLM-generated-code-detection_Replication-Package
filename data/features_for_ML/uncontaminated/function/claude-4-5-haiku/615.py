def handle_exit(sig, frame):
    import sys
    print("\nExiting gracefully...")
    sys.exit(0)
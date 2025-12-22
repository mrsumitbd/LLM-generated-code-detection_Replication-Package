def on_download_complete(success, message):
    if success:
        print(f"Download successful: {message}")
    else:
        print(f"Download failed: {message}")
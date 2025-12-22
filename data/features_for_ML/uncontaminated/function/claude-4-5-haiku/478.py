def on_download_complete(success, message):
    if success:
        print(f"Download completed successfully: {message}")
    else:
        print(f"Download failed: {message}")
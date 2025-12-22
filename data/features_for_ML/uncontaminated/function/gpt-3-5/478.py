def on_download_complete(success, message):
    if success:
        print("Download successful: {}".format(message))
    else:
        print("Download failed: {}".format(message))
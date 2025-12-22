def _compress_spectrals(spectrals_path):
    import os
    import subprocess

    for root, dirs, files in os.walk(spectrals_path):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                subprocess.run(["pyoxipng", file_path])
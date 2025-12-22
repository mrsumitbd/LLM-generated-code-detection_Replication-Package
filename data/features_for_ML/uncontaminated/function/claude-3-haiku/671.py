import os
from pathlib import Path
import subprocess

def _compress_spectrals(spectrals_path):
    """
    Iterate over the spectrals directory and compress them using pyoxipng.
    """
    spectrals_path = Path(spectrals_path)
    for file in spectrals_path.glob('**/*'):
        if file.is_file() and file.suffix in ['.png', '.jpg', '.jpeg']:
            try:
                subprocess.run(['oxipng', '-o', '5', str(file)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error compressing {file}: {e}")
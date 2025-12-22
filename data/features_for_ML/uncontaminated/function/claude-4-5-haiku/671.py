import os
import subprocess
from pathlib import Path


def _compress_spectrals(spectrals_path):
    """
    Iterate over the spectrals directory and compress them using pyoxipng.
    """
    spectrals_dir = Path(spectrals_path)
    
    if not spectrals_dir.exists():
        return
    
    # Find all PNG files in the spectrals directory
    png_files = list(spectrals_dir.glob("*.png"))
    
    for png_file in png_files:
        try:
            # Use oxipng to compress the PNG file
            subprocess.run(
                ["oxipng", "-o", "max", str(png_file)],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error compressing {png_file}: {e}")
        except FileNotFoundError:
            print("oxipng not found. Please install pyoxipng.")
            break
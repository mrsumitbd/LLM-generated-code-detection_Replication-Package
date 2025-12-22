import pathlib
import pyoxipng

def _compress_spectrals(spectrals_path):
    """
    Iterate over the spectrals directory and compress them using pyoxipng.
    """
    spectrals_path = pathlib.Path(spectrals_path)
    if not spectrals_path.is_dir():
        return

    for png_file in spectrals_path.rglob("*.png"):
        try:
            # Compress in place (output_path=None)
            pyoxipng.compress_file(str(png_file), level=9)
        except Exception:
            # If compression fails, skip the file
            continue
import os
import click
import oxipng
from salmon.common.figles import process_files

def _compress_spectrals(spectrals_path):
    """
    Iterate over the spectrals directory and compress them using pyoxipng.
    """
    files = [f for f in os.listdir(spectrals_path) if f.endswith(".png")]
    if not files:
        return

    filepaths = [os.path.join(spectrals_path, f) for f in files]

    process_files(
        filepaths,
        lambda filepath, idx: oxipng.optimize(filepath, level=2, strip=oxipng.StripChunks.all()),
        "Compressing spectral images",
    )

    click.secho("Finished compressing spectrals.", fg="green")
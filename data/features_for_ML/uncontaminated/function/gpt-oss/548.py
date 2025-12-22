from pathlib import Path
import subprocess
import shlex
import sys

def cluster_fasta(path_fasta: Path, dir_out: Path, cutoff: int, threads: int = 4, debug: bool = False) -> Path:
    """
    Clusters the input FASTA file using vsearch.
    :param path_fasta: Input FASTA file
    :param dir_out: Output directory
    :param cutoff: Clustering cutoff (e.g., 0.97 for 97% identity)
    :param threads: Number of threads
    :param debug: If True, the command is logged
    :return: Path to the clustered FASTA file
    """
    # Ensure input exists
    if not path_fasta.is_file():
        raise FileNotFoundError(f"Input FASTA file not found: {path_fasta}")

    # Ensure output directory exists
    dir_out.mkdir(parents=True, exist_ok=True)

    # Define output file
    out_fasta = dir_out / "clustered.fasta"

    # Build vsearch command
    cmd = [
        "vsearch",
        "--cluster_fast",
        str(path_fasta),
        "--id",
        str(cutoff),
        "--centroids",
        str(out_fasta),
        "--threads",
        str(threads),
        "--quiet"
    ]

    if debug:
        print("Running command:", " ".join(shlex.quote(part) for part in cmd), file=sys.stderr)

    # Execute command
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"vsearch failed with exit code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    if not out_fasta.is_file():
        raise RuntimeError(f"Expected output file not created: {out_fasta}")

    return out_fasta
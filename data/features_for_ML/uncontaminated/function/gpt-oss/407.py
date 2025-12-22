import os
import subprocess
import shlex
from pathlib import Path

def run_dbCAN_hmmer(config):
    """
    Run HMMER (hmmscan) against the dbCAN HMM library.

    Parameters
    ----------
    config : dict
        Configuration dictionary. Expected keys:
            - hmmer_path : str
                Path to the hmmscan executable.
            - dbCAN_hmm_path : str
                Path to the dbCAN HMM file.
            - input_fasta : str
                Path to the input FASTA file.
            - output_dir : str
                Directory where output files will be written.
            - evalue : float, optional
                E-value cutoff for hmmscan (default: 1e-5).
            - cpu : int, optional
                Number of CPU threads to use (default: 1).

    Returns
    -------
    str
        Path to the hmmscan tabular output file.
    """
    # Required keys
    required_keys = ["hmmer_path", "dbCAN_hmm_path", "input_fasta", "output_dir"]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: '{key}'")

    hmmer_path = Path(config["hmmer_path"]).expanduser().resolve()
    dbcan_hmm = Path(config["dbCAN_hmm_path"]).expanduser().resolve()
    input_fasta = Path(config["input_fasta"]).expanduser().resolve()
    output_dir = Path(config["output_dir"]).expanduser().resolve()

    # Optional parameters
    evalue = config.get("evalue", 1e-5)
    cpu = config.get("cpu", 1)

    # Validate paths
    if not hmmer_path.is_file():
        raise FileNotFoundError(f"HMMER executable not found: {hmmer_path}")
    if not dbcan_hmm.is_file():
        raise FileNotFoundError(f"dbCAN HMM file not found: {dbcan_hmm}")
    if not input_fasta.is_file():
        raise FileNotFoundError(f"Input FASTA not found: {input_fasta}")

    # Prepare output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output file
    output_tbl = output_dir / "hmmer_dbCAN_tblout.txt"

    # Build command
    cmd = [
        str(hmmer_path),
        "--cpu", str(cpu),
        "--tblout", str(output_tbl),
        "--cut_ga",  # use gathering thresholds if available
        "--noali",   # no alignment output
        "--domtblout", str(output_tbl.with_suffix(".domtblout.txt")),
        str(dbcan_hmm),
        str(input_fasta),
    ]

    # Run hmmscan
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"HMMER failed with exit code {exc.returncode}\n"
            f"Command: {' '.join(shlex.quote(c) for c in cmd)}\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc

    # Optionally filter by e-value
    # The tblout file contains lines starting with '#' as comments.
    # We will keep all lines; filtering can be done downstream.

    return str(output_tbl)
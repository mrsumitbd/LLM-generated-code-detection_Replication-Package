import os
import subprocess
import logging
from typing import Dict, Any

def run_dbCAN_Pfam_null_cgc(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run dbCAN2 with the Pfam null model for a given input FASTA file.

    Parameters
    ----------
    config : dict
        Configuration dictionary that must contain at least the following keys:
        - 'input_fasta' : str
            Path to the input FASTA file.
        - 'output_dir' : str
            Directory where the dbCAN output will be written.
        - 'dbcan_path' : str, optional
            Path to the dbCAN2 executable. Defaults to 'dbCAN2'.
        - 'threads' : int, optional
            Number of threads to use. Defaults to 1.

    Returns
    -------
    dict
        Dictionary containing:
        - 'output' : str
            Path to the generated output file.
        - 'returncode' : int
            Return code from the dbCAN2 process.
    """
    # Extract configuration values with defaults
    input_fasta = config.get("input_fasta")
    output_dir = config.get("output_dir")
    dbcan_path = config.get("dbcan_path", "dbCAN2")
    threads = config.get("threads", 1)

    # Validate required parameters
    if not input_fasta:
        raise ValueError("Missing required configuration key: 'input_fasta'")
    if not output_dir:
        raise ValueError("Missing required configuration key: 'output_dir'")
    if not os.path.isfile(input_fasta):
        raise FileNotFoundError(f"Input FASTA file not found: {input_fasta}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define output file path
    output_file = os.path.join(output_dir, "dbCAN_Pfam_null_cgc.txt")

    # Build the dbCAN2 command
    cmd = [
        dbcan_path,
        "-i",
        input_fasta,
        "-o",
        output_file,
        "-m",
        "Pfam",
        "-t",
        str(threads),
        "--null",
    ]

    # Log the command for debugging
    logging.debug(f"Running dbCAN2 command: {' '.join(cmd)}")

    # Execute the command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        # Log stderr and re-raise
        logging.error(f"dbCAN2 failed with return code {exc.returncode}")
        logging.error(f"stderr: {exc.stderr}")
        raise RuntimeError(f"dbCAN2 execution failed: {exc.stderr}") from exc

    # Return useful information
    return {"output": output_file, "returncode": result.returncode}
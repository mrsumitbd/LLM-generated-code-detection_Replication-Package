import os
from pathlib import Path
from typing import Union
import subprocess

def cluster_fasta(path_fasta: Path, dir_out: Path, cutoff: int, threads: int = 4, debug: bool = False) -> Path:
    """
    Clusters the input FASTA file.
    :param path_fasta: Input FASTA file
    :param dir_out: Output directory
    :param cutoff: Clustering cutoff
    :param threads: Number of threads
    :param debug: If True, the command is logged
    :return: Path to the clustered FASTA file
    """
    dir_out.mkdir(parents=True, exist_ok=True)
    output_file = dir_out / f"{path_fasta.stem}_clustered.fasta"

    command = f"usearch -cluster_fast {path_fasta} -id {cutoff} -centroids {output_file} -threads {threads}"
    if debug:
        print(command)

    subprocess.run(command, shell=True, check=True)

    return output_file
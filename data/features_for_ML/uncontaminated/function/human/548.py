from pathlib import Path
from mist.app.utils.command import Command

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
    path_out = dir_out / path_fasta.name.replace(".fasta", "-clustered.fasta")
    command = Command(
        ' '.join([
            'cd-hit-est',
            '-i', str(path_fasta),
            '-o', str(path_out),
            '-S 0',
            '-d 0',
            '-c', str(cutoff / 100),
            '-T', str(threads)])
    )
    command.run(dir_out, disable_logging=not debug)
    if not command.exit_code == 0:
        raise ValueError(f"error running clustering: {command.stderr}")
    return path_out
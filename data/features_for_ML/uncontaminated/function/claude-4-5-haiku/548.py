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
    import subprocess
    
    dir_out.mkdir(parents=True, exist_ok=True)
    
    output_prefix = dir_out / path_fasta.stem
    clustered_fasta = output_prefix.with_suffix('.fasta')
    
    cmd = [
        'cd-hit',
        '-i', str(path_fasta),
        '-o', str(output_prefix),
        '-c', str(cutoff / 100.0),
        '-T', str(threads),
        '-M', '0'
    ]
    
    if debug:
        print(f"Running command: {' '.join(cmd)}")
    
    subprocess.run(cmd, check=True, capture_output=not debug)
    
    return clustered_fasta
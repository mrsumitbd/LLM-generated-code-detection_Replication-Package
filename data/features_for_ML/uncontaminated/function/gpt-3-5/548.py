def cluster_fasta(path_fasta: Path, dir_out: Path, cutoff: int, threads: int = 4, debug: bool = False) -> Path:
    import subprocess
    import shlex
    import os

    cmd = f"cd-hit -i {path_fasta} -o {dir_out}/clustered.fasta -c {cutoff} -T {threads}"
    if debug:
        print(f"Running command: {cmd}")

    subprocess.run(shlex.split(cmd), check=True)

    return os.path.join(dir_out, "clustered.fasta")
from pathlib import Path

def is_valid_db(dir_in: Path) -> bool:
    """
    Checks if the input directory is a valid typing database.
    :param dir_in: Input directory
    :return: True if valid
    """
    if not (dir_in / 'loci.txt').exists():
        raise FileNotFoundError("'loci.txt' file not found")
    if not (dir_in / 'loci_repr.fasta').exists():
        raise FileNotFoundError("'loci_repr.fasta' file not found")
    return True
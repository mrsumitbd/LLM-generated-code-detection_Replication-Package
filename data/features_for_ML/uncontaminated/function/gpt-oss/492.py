from pathlib import Path

def is_valid_db(dir_in: Path) -> bool:
    """
    Checks if the input directory is a valid typing database.
    A directory is considered a valid typing database if it satisfies at least one of the following
    conditions:
    1. Contains a SQLite database file named either `db.sqlite3` or `db.sqlite`.
    2. Contains a subdirectory named `db` that contains a SQLite database file
       (`db.sqlite3` or `db.sqlite`) and a `metadata.json` file.
    3. Contains a subdirectory named `db` that contains a `words.txt` file and a
       `metadata.json` file.
    4. Contains a `words.txt` file and a `metadata.json` file at the root level.
    5. Contains a `dictionary.json` file and a `metadata.json` file at the root level.
    6. Contains a `config.json` file and a `metadata.json` file at the root level.
    """
    if not isinstance(dir_in, Path):
        dir_in = Path(dir_in)

    if not dir_in.is_dir():
        return False

    # Helper to check for a file
    def has_file(p: Path, name: str) -> bool:
        return (p / name).is_file()

    # 1. SQLite file at root
    if has_file(dir_in, "db.sqlite3") or has_file(dir_in, "db.sqlite"):
        return True

    # 2. SQLite file inside db/ subdirectory
    db_sub = dir_in / "db"
    if db_sub.is_dir():
        if has_file(db_sub, "db.sqlite3") or has_file(db_sub, "db.sqlite"):
            return True
        # 3. words.txt + metadata.json inside db/
        if has_file(db_sub, "words.txt") and has_file(db_sub, "metadata.json"):
            return True

    # 4. words.txt + metadata.json at root
    if has_file(dir_in, "words.txt") and has_file(dir_in, "metadata.json"):
        return True

    # 5. dictionary.json + metadata.json at root
    if has_file(dir_in, "dictionary.json") and has_file(dir_in, "metadata.json"):
        return True

    # 6. config.json + metadata.json at root
    if has_file(dir_in, "config.json") and has_file(dir_in, "metadata.json"):
        return True

    return False
def get_filepath_owners(codeowners: CodeOwners, filepath: str) -> set[str]:
    """
    Return the set of owners for the given filepath according to the provided CodeOwners instance.

    Parameters
    ----------
    codeowners : CodeOwners
        An instance of the CodeOwners class that has already parsed a CODEOWNERS file.
    filepath : str
        The path of the file for which owners should be retrieved.

    Returns
    -------
    set[str]
        A set containing the owners for the specified filepath. If no owners are found,
        an empty set is returned.
    """
    # The CodeOwners class typically provides a method `get_owners_for_path`
    # that returns a list of owner strings (or None if no match is found).
    owners = codeowners.get_owners_for_path(filepath)
    if not owners:
        return set()
    # Ensure we return a set of strings
    return set(str(owner) for owner in owners)
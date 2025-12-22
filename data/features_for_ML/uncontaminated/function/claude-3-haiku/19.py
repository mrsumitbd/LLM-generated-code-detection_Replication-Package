def get_filepath_owners(codeowners: CodeOwners, filepath: str) -> set[str]:
    owners = set()
    for pattern, owner_list in codeowners.items():
        if fnmatch.fnmatch(filepath, pattern):
            owners.update(owner_list)
    return owners
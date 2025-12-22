def get_filepath_owners(codeowners: CodeOwners, filepath: str) -> set[str]:
    owners = set()
    for pattern, owners_list in codeowners.items():
        if pattern == '*' or filepath.startswith(pattern):
            owners.update(owners_list)
    return owners
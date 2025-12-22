from codeowners import CodeOwners

def get_filepath_owners(codeowners: CodeOwners, filepath: str) -> set[str]:
    filename_owners = codeowners.of(filepath)
    return {owner[1] for owner in filename_owners}
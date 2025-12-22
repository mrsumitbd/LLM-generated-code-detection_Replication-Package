def replace_context(match):
    """
    Replacement function for re.sub that extracts the first capturing group
    from the match object. If no capturing group is present, the entire
    matched string is returned unchanged.
    """
    try:
        return match.group(1)
    except IndexError:
        return match.group(0)
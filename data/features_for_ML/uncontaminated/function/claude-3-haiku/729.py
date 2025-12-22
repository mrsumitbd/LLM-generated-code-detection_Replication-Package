def validate_pattern_for_direct_mode(ctx, param, value):
    if not isinstance(value, str):
        raise click.BadParameter(f"'{param.name}' must be a string, not {type(value).__name__}")

    if not value:
        raise click.BadParameter(f"'{param.name}' cannot be an empty string")

    if not all(char in "abcdefghijklmnopqrstuvwxyz0123456789_-" for char in value):
        raise click.BadParameter(f"'{param.name}' can only contain lowercase letters, digits, underscores, and hyphens")

    if value.startswith("-") or value.endswith("-"):
        raise click.BadParameter(f"'{param.name}' cannot start or end with a hyphen")

    if "__" in value:
        raise click.BadParameter(f"'{param.name}' cannot contain consecutive underscores")

    return value
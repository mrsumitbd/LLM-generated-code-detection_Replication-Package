import rich_click as click

def validate_pattern_for_direct_mode(ctx, param, value):
    mode = ctx.params.get("mode")
    if mode == "direct" and not value:
        raise click.BadParameter('--pattern is required when --mode is "direct"')
    return value
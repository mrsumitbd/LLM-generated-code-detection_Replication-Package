import click
from salmon import cfg

def generate_lossy_approval_comment(source_url, filenames, force_prompt_lossy_master=False):
    comment = (
        ""
        if cfg.upload.yes_all and not force_prompt_lossy_master
        else click.prompt(
            click.style(
                "Do you have a comment for the lossy approval report? It is appropriate to "
                "make a note about the source here. Source information from go, gos, and the "
                "queue will be included automatically.",
                fg="cyan",
                bold=True,
            ),
            default="",
        )
    )
    if not (comment or source_url):
        click.secho(
            "This release was not uploaded with go, gos, or the queue, so you must add a comment about the source.",
            fg="red",
        )
        return generate_lossy_approval_comment(source_url, filenames)
    return comment
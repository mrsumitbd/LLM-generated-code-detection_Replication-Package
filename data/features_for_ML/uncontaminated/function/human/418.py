from os import listdir, makedirs, path
import click

def check_if_migration_is_needed():
    current_version = get_current_version()
    most_recent_mig = sorted(f for f in listdir(MIG_DIR) if f.endswith(".sql"))[-1:][0]
    if path.exists(OLD_DB_PATH):
        click.secho(
            f"The database needs to be moved to the new directory ({DB_PATH}). Please run `salmon migrate`.\n",
            fg="red",
            bold=True,
        )
    try:
        mig_version = int(most_recent_mig[:4])
    except TypeError:
        click.secho(
            f"\n{most_recent_mig} is improperly named. It must start with a four digit integer.",
            fg="red",
        )
        raise click.Abort from None
    if mig_version > current_version:
        click.secho(
            "The database needs updating. Please run `salmon migrate`.\n",
            fg="red",
            bold=True,
        )
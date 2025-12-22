from fabric_cli.core.fab_commands import Command
from argparse import Namespace
from fabric_cli.commands.fs import fab_fs_import as fs_import
from fabric_cli.core import fab_handle_context as handle_context

def import_command(args: Namespace) -> None:
    context = handle_context.get_command_context(args.path, raise_error=False)
    context.check_command_support(Command.FS_IMPORT)
    fs_import.exec_command(args, context)
from fabric_cli.commands.tables import fab_tables_schema as tables_schema
from argparse import Namespace
from fabric_cli.core import fab_handle_context as handle_context
from fabric_cli.core.fab_commands import Command
from fabric_cli.core.hiearchy.fab_onelake_element import OneLakeItem
from fabric_cli.utils import fab_cmd_table_utils as utils_table
from fabric_cli.utils import fab_ui as utils_ui

def schema_command(args: Namespace) -> None:
    context = handle_context.get_command_context(args.path)
    context.check_command_support(Command.TABLE_SCHEMA)
    assert isinstance(context, OneLakeItem)
    utils_table.add_table_props_to_args(args, context)
    utils_ui.print_grey(f"Getting schema for '{args.table_name}' table...")
    tables_schema.exec_command(args)
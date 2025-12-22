from fabric_cli.core import fab_constant
from argparse import Namespace, _SubParsersAction
from fabric_cli.commands.fs import fab_fs as fs
from fabric_cli.utils import fab_error_parser as utils_error_parser

def register_exists_parser(subparsers: _SubParsersAction) -> None:
    exists_examples = [
        "# check if a workspace exists",
        "$ exists /ws1.Workspace\n",
        "# check if an item exists",
        "$ exists /ws1.Workspace/lh1.Lakehouse",
    ]

    exists_parser = subparsers.add_parser(
        "exists",
        help=fab_constant.COMMAND_FS_EXISTS_DESCRIPTION,
        fab_examples=exists_examples,
        fab_learnmore=["_"],
    )
    exists_parser.add_argument("path", nargs="+", type=str, help="Directory path")

    exists_parser.usage = f"{utils_error_parser.get_usage_prog(exists_parser)}"
    exists_parser.set_defaults(func=fs.exists_command)
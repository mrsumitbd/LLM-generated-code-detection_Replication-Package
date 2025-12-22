from fabric_cli.core import fab_constant
from argparse import Namespace, _SubParsersAction
from fabric_cli.commands.fs import fab_fs as fs
from fabric_cli.utils import fab_error_parser as utils_error_parser

def register_stop_parser(subparsers: _SubParsersAction) -> None:
    stop_examples = [
        "# stop a capacity",
        "$ stop .capacities/capac1.Capacity .\n",
        "# stop mirroring",
        "$ stop ws1.Workspace/mir1.MirroredDatabase -f",
    ]

    stop_parser = subparsers.add_parser(
        "stop",
        help=fab_constant.COMMAND_FS_STOP_DESCRIPTION,
        fab_examples=stop_examples,
        fab_learnmore=["_"],
    )
    stop_parser.add_argument("path", nargs="+", type=str, help="Directory path")
    stop_parser.add_argument(
        "-f", "--force", required=False, action="store_true", help="Force. Optional"
    )

    stop_parser.usage = f"{utils_error_parser.get_usage_prog(stop_parser)}"
    stop_parser.set_defaults(func=fs.stop_command)
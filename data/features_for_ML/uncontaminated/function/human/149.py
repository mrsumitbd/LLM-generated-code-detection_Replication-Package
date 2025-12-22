from argparse import Namespace
from fabric_cli.client import fab_api_client as fabric_api
from fabric_cli.utils import fab_ui as utils_ui

def _do_start_resource(args: Namespace, verbose: bool = True) -> bool:
    if verbose:
        utils_ui.print_grey(f"Starting '{args.name}'...")
    response = fabric_api.do_request(args)

    return _validate_success_and_print_on_verbose(
        args, "started", response.status_code, verbose
    )
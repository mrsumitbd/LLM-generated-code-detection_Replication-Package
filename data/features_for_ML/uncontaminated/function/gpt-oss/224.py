from argparse import _SubParsersAction

# Try to import the real handler; fall back to a simple implementation if it
# cannot be imported.  This keeps the parser functional even if the
# surrounding package is incomplete.
try:
    # The handler is expected to be defined in a sibling module named
    # `exists.py` and to accept a namespace object with a `path` attribute.
    from .exists import exists as _exists_handler
except Exception:  # pragma: no cover
    def _exists_handler(args):
        """Fallback handler that simply prints whether the given path exists."""
        import os
        print(os.path.exists(args.path))

def register_exists_parser(subparsers: _SubParsersAction) -> None:
    """
    Register the ``exists`` sub‑command parser.

    The command accepts a single positional argument ``path`` and
    dispatches to the handler function defined in ``file.exists``.
    """
    parser = subparsers.add_parser(
        "exists",
        help="Check whether a file or directory exists",
    )
    parser.add_argument(
        "path",
        help="Path to the file or directory to check",
    )
    parser.set_defaults(func=_exists_handler)
from argparse import Namespace
import json
import sys
from pathlib import Path


def schema_command(args: Namespace) -> None:
    """
    Handle the `schema` subcommand.

    The command supports two simple modes:

    * ``--dump`` – generate a minimal JSON schema and write it to
      ``--output`` if supplied, otherwise print to stdout.
    * ``--load`` – read a JSON schema from ``--input`` and print a
      confirmation message.

    If neither ``--dump`` nor ``--load`` is supplied, a short usage
    message is printed.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command‑line arguments.  Expected attributes:

        * ``dump`` (bool) – whether to generate a schema.
        * ``load`` (bool) – whether to load a schema.
        * ``output`` (str | None) – file path for the dumped schema.
        * ``input`` (str | None) – file path for the schema to load.
    """
    # Dump mode -------------------------------------------------------------
    if getattr(args, "dump", False):
        # Create a very small dummy schema
        schema = {
            "title": "Dummy Schema",
            "type": "object",
            "properties": {},
        }

        output_path = getattr(args, "output", None)
        if output_path:
            try:
                Path(output_path).write_text(json.dumps(schema, indent=2))
            except OSError as exc:
                print(f"Error writing schema to {output_path!r}: {exc}", file=sys.stderr)
        else:
            print(json.dumps(schema, indent=2))
        return

    # Load mode --------------------------------------------------------------
    if getattr(args, "load", False):
        input_path = getattr(args, "input", None)
        if not input_path:
            print("Error: --input is required when using --load", file=sys.stderr)
            return

        try:
            raw = Path(input_path).read_text()
            schema = json.loads(raw)
        except Exception as exc:
            print(f"Error loading schema from {input_path!r}: {exc}", file=sys.stderr)
            return

        # Just confirm that we loaded something
        print("Loaded schema:")
        print(json.dumps(schema, indent=2))
        return

    # No action specified -----------------------------------------------
    print("No action specified. Use --dump to generate a schema or --load to read one.")
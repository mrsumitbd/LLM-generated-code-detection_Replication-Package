import argparse
import textwrap

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="vfio-assist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            Smart VFIO diagnostics & remediation tool.
            --------------------------------------------------------------------
            Most commands require *root* - either run with sudo or prefix
            privileged sub‑steps with sudo when prompted.
            """,
        ),
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-d", "--device", dest="device_bdf", help="Target PCIe BDF (0000:01:00.0)"
    )
    common.add_argument(
        "--quiet", action="store_true", help="Silence info logs (warnings still shown)"
    )

    sub.add_parser(
        "diagnose", parents=[common], help="Run diagnostics and print report"
    )
    fix_p = sub.add_parser(
        "fix", parents=[common], help="Attempt automatic remediation"
    )
    fix_p.add_argument(
        "-y", "--yes", action="store_true", help="Run fixes without confirmation"
    )

    sub.add_parser(
        "script", parents=[common], help="Output a shell script that would fix issues"
    )
    sub.add_parser(
        "json", parents=[common], help="Machine‑readable JSON report (stdout)"
    )

    return parser.parse_args(argv)
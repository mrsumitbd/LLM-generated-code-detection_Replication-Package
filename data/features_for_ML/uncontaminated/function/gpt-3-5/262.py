import os

def warn_if_run_as_root() -> None:
    if os.geteuid() == 0 and not os.getenv('VIRTUAL_ENV'):
        print("WARNING: Running this script as root outside of a virtual environment may harm your system.")
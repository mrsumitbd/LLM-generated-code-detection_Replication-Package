import subprocess
import sys
from colorama import Fore

def run_command(cmd, description=None):
    if description:
        print(f'{Fore.CYAN}{description}{Fore.RESET}')
    try:
        subprocess.run(cmd, shell=True, check=True)
        print()
    except subprocess.CalledProcessError as e:
        print(f'{Fore.RED}Command failed, if fixes attempted, run again: {cmd}{Fore.RESET}')
        sys.exit(e.returncode)
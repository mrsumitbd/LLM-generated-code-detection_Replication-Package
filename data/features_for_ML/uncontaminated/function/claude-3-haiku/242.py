import subprocess

def run_command(cmd, description=None):
    try:
        if description:
            print(f"Running command: {description}")
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        print(output.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return 1
    return 0
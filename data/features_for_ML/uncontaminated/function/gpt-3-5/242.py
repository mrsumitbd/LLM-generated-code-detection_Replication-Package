def run_command(cmd, description=None):
    import subprocess
    import shlex
    
    if description:
        print(description)
    
    cmd_list = shlex.split(cmd)
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if output:
        print(output.decode())
    
    if error:
        print(error.decode())
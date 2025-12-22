import time

# A placeholder for command status storage.
# In a real system this would be provided by the surrounding framework.
COMMANDS = {}

def wait_for_command(command_id: int):
    """
    Wait until the command with the given ID reaches a terminal state.

    The function polls the global COMMANDS dictionary for the status of the
    command. It considers the command finished when its status is either
    'completed' or 'succeeded'. If the status becomes 'failed' or 'error',
    a RuntimeError is raised. If the command is not found or does not
    finish within the timeout, a ValueError or TimeoutError is raised
    respectively.

    Parameters
    ----------
    command_id : int
        The identifier of the command to wait for.

    Raises
    ------
    ValueError
        If the command ID is not present in the COMMANDS dictionary.
    RuntimeError
        If the command fails.
    TimeoutError
        If the command does not finish within the timeout period.
    """
    # Configuration
    timeout = 30.0          # seconds
    poll_interval = 0.1     # seconds

    start_time = time.time()

    while True:
        cmd = COMMANDS.get(command_id)
        if cmd is None:
            raise ValueError(f"Command {command_id} not found")

        status = cmd.get("status")
        if status in ("completed", "succeeded"):
            return
        if status in ("failed", "error"):
            raise RuntimeError(f"Command {command_id} failed with status '{status}'")

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for command {command_id}")

        time.sleep(poll_interval)
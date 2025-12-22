def wait_for_command(command_id: int):
    import time
    import threading
    
    # Global dictionary to store command results
    if not hasattr(wait_for_command, '_commands'):
        wait_for_command._commands = {}
        wait_for_command._lock = threading.Lock()
    
    # Wait for the command to be processed
    timeout = 30  # 30 second timeout
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        with wait_for_command._lock:
            if command_id in wait_for_command._commands:
                result = wait_for_command._commands.pop(command_id)
                return result
        time.sleep(0.1)
    
    raise TimeoutError(f"Command {command_id} did not complete within {timeout} seconds")
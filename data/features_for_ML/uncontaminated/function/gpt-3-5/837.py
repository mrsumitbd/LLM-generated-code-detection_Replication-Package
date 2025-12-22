def wait_for_command(command_id: int):
    if command_id == 1:
        print("Waiting for command 1...")
    elif command_id == 2:
        print("Waiting for command 2...")
    elif command_id == 3:
        print("Waiting for command 3...")
    else:
        print("Waiting for unknown command...")
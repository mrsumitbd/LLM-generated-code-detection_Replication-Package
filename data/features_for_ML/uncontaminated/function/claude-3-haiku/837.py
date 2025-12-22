import time

def wait_for_command(command_id: int):
    while True:
        try:
            with open(f"command_{command_id}.txt", "r") as file:
                command = file.read().strip()
                if command == "execute":
                    return
        except FileNotFoundError:
            pass
        time.sleep(1)
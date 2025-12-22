class RotavapOne:

    def __init__(self, port, rate=9600):
        self.port = port
        self.rate = rate

    def cmd_write(self, cmd):
        print(f"Writing command: {cmd}")

    def set_rotate_time(self, time):
        print(f"Setting rotate time to: {time} seconds")

    def set_pump_time(self, time):
        print(f"Setting pump time to: {time} seconds")

    def set_timer(self, command):
        print(f"Setting timer with command: {command}")

    def main_loop(self):
        print("Entering main loop...")

# Example usage:
rotavap = RotavapOne("COM1")
rotavap.cmd_write("start")
rotavap.set_rotate_time(60)
rotavap.set_pump_time(30)
rotavap.set_timer("stop")
rotavap.main_loop()
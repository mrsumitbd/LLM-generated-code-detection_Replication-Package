import serial

class RotavapOne:
    def __init__(self, port, rate=9600):
        self.ser = serial.Serial(port, rate)

    def cmd_write(self, cmd):
        self.ser.write(cmd.encode())
        response = self.ser.readline().decode().strip()
        return response

    def set_rotate_time(self, time):
        cmd = f"RT{time:04d}"
        self.cmd_write(cmd)

    def set_pump_time(self, time):
        cmd = f"PT{time:04d}"
        self.cmd_write(cmd)

    def set_timer(self, command):
        self.cmd_write(command)

    def main_loop(self):
        while True:
            command = input("Enter command ('q' to quit): ")
            if command.lower() == 'q':
                break
            self.set_timer(command)
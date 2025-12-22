import serial
import time

class RotavapOne:

    def __init__(self, port, rate=9600):
        self.port = port
        self.rate = rate
        self.serial = serial.Serial(port, rate, timeout=1)
        time.sleep(2)

    def cmd_write(self, cmd):
        if isinstance(cmd, str):
            cmd = cmd.encode()
        self.serial.write(cmd)
        self.serial.write(b'\r\n')

    def set_rotate_time(self, time):
        cmd = f"ROTATE_TIME {time}"
        self.cmd_write(cmd)

    def set_pump_time(self, time):
        cmd = f"PUMP_TIME {time}"
        self.cmd_write(cmd)

    def set_timer(self, command):
        cmd = f"TIMER {command}"
        self.cmd_write(cmd)

    def main_loop(self):
        try:
            while True:
                if self.serial.in_waiting > 0:
                    response = self.serial.readline().decode().strip()
                    if response:
                        print(f"Response: {response}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Exiting main loop")
        finally:
            self.serial.close()
import time

try:
    import serial
except ImportError:
    serial = None


class RotavapOne:
    """
    Simple interface to a RotavapOne device over a serial port.
    """

    def __init__(self, port, rate=9600):
        """
        Initialise the serial connection.

        :param port: Serial port name (e.g. 'COM3' or '/dev/ttyUSB0')
        :param rate: Baud rate (default 9600)
        """
        self.port = port
        self.rate = rate
        self.ser = None

        if serial is None:
            raise RuntimeError("pyserial is required but not installed")

        try:
            self.ser = serial.Serial(port, rate, timeout=1)
        except Exception as exc:
            raise RuntimeError(f"Could not open serial port {port}: {exc}")

    def cmd_write(self, cmd):
        """
        Send a command string to the device.

        :param cmd: Command string (without newline)
        :return: True if sent successfully, False otherwise
        """
        if not self.ser or not self.ser.is_open:
            print("Serial port not open")
            return False

        try:
            self.ser.write((cmd + "\n").encode("utf-8"))
            return True
        except Exception as exc:
            print(f"Error writing to serial: {exc}")
            return False

    def set_rotate_time(self, time_sec):
        """
        Set the rotation time.

        :param time_sec: Rotation time in seconds
        :return: Result of cmd_write
        """
        cmd = f"ROTATE {time_sec}"
        return self.cmd_write(cmd)

    def set_pump_time(self, time_sec):
        """
        Set the pump time.

        :param time_sec: Pump time in seconds
        :return: Result of cmd_write
        """
        cmd = f"PUMP {time_sec}"
        return self.cmd_write(cmd)

    def set_timer(self, command):
        """
        Send a timer command.

        :param command: Timer command string
        :return: Result of cmd_write
        """
        cmd = f"TIMER {command}"
        return self.cmd_write(cmd)

    def main_loop(self):
        """
        Main loop that reads from the serial port and prints any incoming data.
        Press Ctrl+C to exit.
        """
        if not self.ser or not self.ser.is_open:
            print("Serial port not open, cannot enter main loop")
            return

        print("Entering main loop. Press Ctrl+C to exit.")
        try:
            while True:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode("utf-8").strip()
                    if line:
                        print(f"Received: {line}")
                # Small sleep to avoid busy‑waiting
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting main loop.")
        finally:
            self.ser.close()
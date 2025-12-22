import time

def run_until_status(ser, DEVICE_ADDRESS, status_info: str, max_time=10):
    """
    Poll a device via a serial connection until a line containing `status_info`
    is received or until `max_time` seconds have elapsed.

    Parameters
    ----------
    ser : serial.Serial
        The serial connection to the device.
    DEVICE_ADDRESS : int or str
        The address of the device to query.
    status_info : str
        The substring that must appear in a response line to consider the
        status as reached.
    max_time : float, optional
        Maximum number of seconds to wait for the status. Default is 10.

    Returns
    -------
    str or None
        The first line that contains `status_info`, or `None` if the timeout
        expires before such a line is received.
    """
    # Ensure the input buffer is clear before we start polling
    try:
        ser.reset_input_buffer()
    except AttributeError:
        # Some serial implementations may not expose this method
        pass

    # Send a status request.  The exact command may vary; this is a common
    # convention.  If the device uses a different protocol, adjust accordingly.
    try:
        cmd = f"GET_STATUS {DEVICE_ADDRESS}\n"
        ser.write(cmd.encode())
    except Exception:
        # If we cannot write, just return None
        return None

    start = time.time()
    while (time.time() - start) < max_time:
        try:
            line_bytes = ser.readline()
            if not line_bytes:
                # No data received; give the device a moment to respond
                time.sleep(0.05)
                continue
            line = line_bytes.decode(errors='ignore').strip()
            if status_info in line:
                return line
        except Exception:
            # Ignore read errors and continue polling
            pass
        # Small delay to avoid busy‑waiting
        time.sleep(0.01)

    # Timeout reached without seeing the desired status
    return None
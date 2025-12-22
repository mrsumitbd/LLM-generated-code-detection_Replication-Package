import time
import serial

def run_until_status(ser, DEVICE_ADDRESS, status_info: str, max_time=10):
    """
    Run a command on a serial device until a specific status is achieved.
    
    Args:
        ser: Serial connection object
        DEVICE_ADDRESS: Address of the device
        status_info: Status string to wait for
        max_time: Maximum time to wait in seconds
    
    Returns:
        True if status achieved, False if timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < max_time:
        try:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8', errors='ignore').strip()
                if status_info in response:
                    return True
        except Exception:
            pass
        
        time.sleep(0.1)
    
    return False
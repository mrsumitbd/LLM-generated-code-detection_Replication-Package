def run_until_status(ser, DEVICE_ADDRESS, status_info: str, max_time=10):
    import time
    
    start_time = time.time()
    while True:
        ser.write(f"{DEVICE_ADDRESS} {status_info}\n".encode())
        response = ser.readline().decode().strip()
        if response == status_info:
            return True
        if time.time() - start_time > max_time:
            return False
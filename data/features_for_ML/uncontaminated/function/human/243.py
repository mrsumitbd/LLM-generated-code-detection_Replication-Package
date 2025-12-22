import time

def run_until_status(ser, DEVICE_ADDRESS, status_info: str, max_time=10):
    start_time = time.time()
    while True:
        ret = run_get_status(ser, DEVICE_ADDRESS)
        if status_info in ret:
            break
        if time.time() - start_time > max_time:
            print(f"状态未达到 {status_info} 超时")
            return False
        time.sleep(0.05)
    return True
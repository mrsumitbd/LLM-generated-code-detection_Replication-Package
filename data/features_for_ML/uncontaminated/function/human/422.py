from datetime import datetime

def log(msg: str, return_line=False, pre_return_line=False, *args, **kwargs):
    if pre_return_line:
        print("")

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {msg}", *args, **kwargs)

    if return_line:
        print("")
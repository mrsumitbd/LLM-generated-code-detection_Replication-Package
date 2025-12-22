from datetime import datetime, time, timedelta

def is_current_time_within_range(time_range_str: str):
    start_str, end_str = time_range_str.split("~")
    time_format = "%H:%M:%S"

    start_time = datetime.strptime(start_str.strip(), time_format).time()
    end_time = datetime.strptime(end_str.strip(), time_format).time()
    now = datetime.now().time()

    if end_time < start_time:
        return now >= start_time or now <= end_time
    else:
        return start_time <= now <= end_time
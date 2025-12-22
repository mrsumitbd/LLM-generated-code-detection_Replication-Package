def is_current_time_within_range(time_range_str: str):
    import datetime

    current_time = datetime.datetime.now().time()
    start_time_str, end_time_str = time_range_str.split('-')
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

    if start_time <= current_time <= end_time:
        return True
    else:
        return False
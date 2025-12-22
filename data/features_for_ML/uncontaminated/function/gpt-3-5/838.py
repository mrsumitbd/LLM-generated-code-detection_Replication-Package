def get_log_timestamp_prefix(self) -> str:
    import datetime
    return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
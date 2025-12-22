def parse_log_calypso(log: str, test_spec: "TestSpec") -> dict[str, str]:
    log_lines = log.split('\n')
    parsed_data = {}
    
    for line in log_lines:
        if test_spec.test_name in line:
            key_value = line.split(':')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                parsed_data[key] = value
    
    return parsed_data
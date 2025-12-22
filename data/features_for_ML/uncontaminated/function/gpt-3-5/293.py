def format_alert(feature: dict) -> str:
    alert_str = ""
    for key, value in feature.items():
        alert_str += f"{key}: {value}\n"
    return alert_str
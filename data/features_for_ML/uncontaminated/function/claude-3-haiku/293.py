def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    alert_type = feature.get('type', 'Unknown')
    alert_severity = feature.get('severity', 'Unknown')
    alert_description = feature.get('description', 'No description provided')
    alert_timestamp = feature.get('timestamp', 'Unknown')

    return f"Alert Type: {alert_type}\nSeverity: {alert_severity}\nDescription: {alert_description}\nTimestamp: {alert_timestamp}"
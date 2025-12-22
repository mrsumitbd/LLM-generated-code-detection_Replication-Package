import anthropic
import json


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    client = anthropic.Anthropic()
    
    feature_json = json.dumps(feature, indent=2)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Format the following alert feature into a clear, readable string. 
The output should be a concise summary that includes the key information from the alert.
Alert feature:
{feature_json}

Please provide only the formatted alert string, without any additional explanation."""
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    test_feature = {
        "type": "Feature",
        "properties": {
            "alert_id": "ALT001",
            "severity": "high",
            "message": "System CPU usage exceeded 90%",
            "timestamp": "2024-01-15T10:30:00Z",
            "affected_system": "Production Server 1",
            "status": "active"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [40.7128, -74.0060]
        }
    }
    
    formatted = format_alert(test_feature)
    print("Formatted Alert:")
    print(formatted)
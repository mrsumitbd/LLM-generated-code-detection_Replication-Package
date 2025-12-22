import anthropic
import json
import os


def dump_distro_mapping(path: str):
    """
    Dump a distribution mapping to a file using Claude API.
    
    This function uses the Anthropic API to generate a distribution mapping
    and saves it to the specified path.
    
    Args:
        path: The file path where the distribution mapping should be saved
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Generate a JSON mapping of Linux distributions to their package managers. Include at least 10 distributions with their primary package managers. Return only valid JSON."
            }
        ]
    )
    
    response_text = message.content[0].text
    
    try:
        distro_mapping = json.loads(response_text)
    except json.JSONDecodeError:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            distro_mapping = json.loads(response_text[json_start:json_end])
        else:
            distro_mapping = {"error": "Could not parse response"}
    
    with open(path, 'w') as f:
        json.dump(distro_mapping, f, indent=2)


if __name__ == "__main__":
    dump_distro_mapping("distro_mapping.json")
    print("Distribution mapping saved to distro_mapping.json")
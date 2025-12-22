import anthropic
import json
import os
import subprocess


def get_role_binding_events(path, context, namespace, role_binding_name):
    """
    Get events related to a specific RoleBinding in Kubernetes using Claude.
    
    Args:
        path: Path to kubeconfig file
        context: Kubernetes context to use
        namespace: Kubernetes namespace
        role_binding_name: Name of the RoleBinding
    
    Returns:
        Events related to the RoleBinding
    """
    
    # Get RoleBinding details
    cmd = [
        "kubectl",
        "--kubeconfig", path,
        "--context", context,
        "-n", namespace,
        "get", "rolebinding", role_binding_name,
        "-o", "json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error getting RoleBinding: {result.stderr}"
    
    role_binding_data = json.loads(result.stdout)
    
    # Get events for the RoleBinding
    cmd = [
        "kubectl",
        "--kubeconfig", path,
        "--context", context,
        "-n", namespace,
        "get", "events",
        "--field-selector", f"involvedObject.name={role_binding_name},involvedObject.kind=RoleBinding",
        "-o", "json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error getting events: {result.stderr}"
    
    events_data = json.loads(result.stdout)
    
    # Use Claude to analyze the RoleBinding and events
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"""Analyze the following Kubernetes RoleBinding and its associated events:

RoleBinding Details:
{json.dumps(role_binding_data, indent=2)}

Associated Events:
{json.dumps(events_data, indent=2)}

Please provide:
1. A summary of the RoleBinding configuration
2. Any important events or warnings
3. Analysis of the role binding's purpose and permissions
4. Any potential issues or recommendations"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: python solution.py <kubeconfig_path> <context> <namespace> <role_binding_name>")
        sys.exit(1)
    
    path = sys.argv[1]
    context = sys.argv[2]
    namespace = sys.argv[3]
    role_binding_name = sys.argv[4]
    
    result = get_role_binding_events(path, context, namespace, role_binding_name)
    print(result)
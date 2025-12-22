import anthropic
import os


def save_ros_msg_file(model_name, ros_msg_definition):
    """
    Save a ROS message definition to a file using Claude to generate the content.
    
    Args:
        model_name: The name of the ROS message model (e.g., "Point", "Twist")
        ros_msg_definition: The ROS message definition string
    
    Returns:
        The path to the saved file
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Given the following ROS message model name and definition, generate a properly formatted ROS message file content.

Model name: {model_name}
Definition: {ros_msg_definition}

Please generate the complete ROS message file content that would be saved in a .msg file. Include proper formatting and any necessary comments."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    file_content = message.content[0].text
    
    os.makedirs("ros_msgs", exist_ok=True)
    
    file_path = f"ros_msgs/{model_name}.msg"
    
    with open(file_path, "w") as f:
        f.write(file_content)
    
    return file_path


if __name__ == "__main__":
    model_name = "CustomPoint"
    ros_msg_definition = "A custom point message with x, y, z coordinates and a timestamp"
    
    file_path = save_ros_msg_file(model_name, ros_msg_definition)
    print(f"ROS message file saved to: {file_path}")
    
    with open(file_path, "r") as f:
        print("\nFile content:")
        print(f.read())
import os

def save_ros_msg_file(model_name, ros_msg_definition):
    """
    Save a ROS message definition to a .msg file.

    Parameters
    ----------
    model_name : str
        The name of the message (without extension). It will be used as the file name.
    ros_msg_definition : str
        The content of the ROS message definition.

    Returns
    -------
    str
        The absolute path to the created .msg file.

    Raises
    ------
    ValueError
        If `model_name` or `ros_msg_definition` is empty or None.
    """
    if not model_name or not isinstance(model_name, str):
        raise ValueError("model_name must be a non-empty string")
    if not ros_msg_definition or not isinstance(ros_msg_definition, str):
        raise ValueError("ros_msg_definition must be a non-empty string")

    # Ensure the directory exists
    msg_dir = os.path.join(os.getcwd(), "msg")
    os.makedirs(msg_dir, exist_ok=True)

    # Sanitize the file name
    safe_name = os.path.basename(model_name).strip()
    if not safe_name:
        raise ValueError("model_name must contain a valid file name")

    file_path = os.path.join(msg_dir, f"{safe_name}.msg")

    # Write the definition to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ros_msg_definition.rstrip() + "\n")

    return os.path.abspath(file_path)
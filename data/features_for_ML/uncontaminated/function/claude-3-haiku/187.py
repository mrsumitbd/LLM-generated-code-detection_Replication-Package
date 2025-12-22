def save_ros_msg_file(model_name, ros_msg_definition):
    import os

    # Create the directory for the ROS message file if it doesn't exist
    msg_dir = os.path.join('ros', 'msg')
    if not os.path.exists(msg_dir):
        os.makedirs(msg_dir)

    # Save the ROS message definition to a file
    msg_file_path = os.path.join(msg_dir, f"{model_name}.msg")
    with open(msg_file_path, 'w') as msg_file:
        msg_file.write(ros_msg_definition)
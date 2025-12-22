def save_ros_msg_file(model_name, ros_msg_definition):
    file_name = model_name + ".msg"
    with open(file_name, "w") as file:
        file.write(ros_msg_definition)
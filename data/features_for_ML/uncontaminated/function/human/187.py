import os

def save_ros_msg_file(model_name, ros_msg_definition):
    msg_file_path = os.path.join(ROS_MSG_DIR, f'{model_name}.msg')
    os.makedirs(ROS_MSG_DIR, exist_ok=True)
    with open(msg_file_path, 'w') as msg_file:
        msg_file.write(ros_msg_definition)
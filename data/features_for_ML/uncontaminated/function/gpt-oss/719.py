from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    talker_node = Node(
        package='demo_nodes_py',
        executable='talker',
        name='talker',
        output='screen'
    )
    return LaunchDescription([talker_node])
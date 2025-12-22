from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for the ROS 2 node."""
    return LaunchDescription([
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='talker',
            output='screen'
        ),
        Node(
            package='demo_nodes_cpp',
            executable='listener',
            name='listener',
            output='screen'
        ),
    ])
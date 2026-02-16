from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='report_one_pkg', executable='mygui', name='gui'),
        Node(package='report_one_pkg', executable='mymode', name='service'),
        Node(package='report_one_pkg', executable='mymoving', name='action'),
    ])

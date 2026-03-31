from launch import LaunchDescription
from launch_ros.actions import Node


Serial_bridge_node = Node(
            package='scooby_firmware',
            executable='serial_bridge',
            name='serial_bridge',
            output='screen',
        )

Camera_publisher_node = Node(
            package='scooby_camera',
            executable='camera_publisher',
            name='camera_publisher',
            output='screen',
        )


def generate_launch_description():
    return LaunchDescription([
        Serial_bridge_node,
        Camera_publisher_node
    ])
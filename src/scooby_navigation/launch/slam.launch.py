import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # nav2_bringup and scooby_navigation package paths
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    scooby_nav_dir = FindPackageShare('scooby_navigation')
    nav2_params_path = PathJoinSubstitution([scooby_nav_dir, 'config', 'nav2_params.yaml'])
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true.'
    )
    
    
    #SLAM Toolbox Node,
    slam_node = Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'mode': 'mapping',
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_footprint',
                'scan_topic': '/scan',
                'transform_timeout': 0.5,
                'tf_buffer_duration': 30.0,
                'scan_queue_size': 100,
            }],
        )

    #Navigation Node,
    # this launch file is used to start the navigation stack
    navigation_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'navigation_launch.py'])
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'params_file': nav2_params_path
            }.items()
        )

    # Give SLAM a short head start to publish map->odom before planner startup.
    delayed_navigation_launch = TimerAction(
        period=3.0,
        actions=[navigation_launch]
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        slam_node,
        delayed_navigation_launch
    ])

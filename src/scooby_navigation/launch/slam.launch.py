import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # nav2_bringup and scooby_navigation package paths
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    scooby_nav_dir = FindPackageShare('scooby_navigation')
    nav2_params_path = PathJoinSubstitution([scooby_nav_dir, 'config', 'nav2_params.yaml'])
    
    
    #SLAM Toolbox Node,
    slam_node = Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{'use_sim_time': True}],
        )
    #Navigation Node,
    # this launch file is used to start the navigation stack
    navigation_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'navigation_launch.py'])
            ),
            launch_arguments={
                'use_sim_time': 'true', 
                'params_file': nav2_params_path
            }.items()
        )
    
    return LaunchDescription([
        slam_node,
        navigation_launch
    ])

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

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
    # Map path
    map_path = PathJoinSubstitution([scooby_nav_dir, 'maps', 'Mappa1.yaml'])

    #Navigation Node,
    # this launch file is used to start the navigation stack with AMCL localization.
    navigation_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'navigation_launch.py'])
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'params_file': nav2_params_path,
                'map': map_path,
            }.items()
        )
    
    #AMCL Localization Node,
    # this launch file is used to start the AMCL localization node 
    amcl_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'localization_launch.py'])
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'map': map_path,
                'params_file': nav2_params_path
            }.items()
        )
    

    
    return LaunchDescription([
        use_sim_time_arg,
        navigation_launch,
        amcl_launch
    ])
# scooby Navigation Package

This package contains the necessary launch files for the autonomous navigation

### Launch files


1. **SLAM**
   ```bash
   ros2 launch scooby_navigation slam.launch.py
   ```
   Save the map with:
   ```bash
   ros2 run nav2_map_server map_saver_cli -f <maps_name>
   ```

2. **AMCL**
   Pay attention to the map path:
   ```bash
   ros2 launch scooby_navigation amcl.launch.py
   ```





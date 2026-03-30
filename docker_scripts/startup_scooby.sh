#/bin/bash
# Script di avvio automatico per Scooby-Bot
set -e
cd /home/scobybot/Scooby_Bot/docker_scripts
./docker_run_container.sh
cd /home/pi/Scooby-Bot
colcon build
source install/setup.bash
ros2 run scooby_firmware serial_bridge

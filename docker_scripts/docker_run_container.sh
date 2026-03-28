#!/bin/bash
THISDIR=$(dirname "$(realpath "$0")")

IMAGE_NAME="scooby_real_image"
IMAGE_ID=$(docker images -q "$IMAGE_NAME")
CNT_NAME="scooby_real_cnt"

# Start the container with options required to run ROS2 and Gazebo with GUI
xhost +local:root
docker run --rm -it --net=host \
	--env="DISPLAY=$DISPLAY" \
	--env="QT_X11_NO_MITSHM=1" \
	--env="XDG_RUNTIME_DIR=/tmp/runtime-root" \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
	--volume="$THISDIR/../src:/root/ros2_ws/src:rw" \
	--device=/dev/dri:/dev/dri \
	--privileged \
	"${DOCKER_VOLUMES_ARGS[@]}" \
	--name="$CNT_NAME" \
	--workdir "/root/ros2_ws" \
	"$IMAGE_NAME" \
	bash

xhost -local:root

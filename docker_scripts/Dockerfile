# Utilizziamo l'immagine ufficiale ROS2 Humble base (compatibile nativamente con ARM64 del RPi5)
FROM ros:humble-ros-base

# Impostazioni ambiente
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    HOME=/root \
    ROS_DISTRO=humble

WORKDIR /root

# Installazione dipendenze di base, colcon, tools seriali e pacchetti ROS2 necessari
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    python3-serial \
    libserial-dev \
    git \
    udev \
    python3-colcon-common-extensions \
    python3-vcstool \
    python3-opencv \
    ros-humble-geometry-msgs \
    ros-humble-std-msgs \
    ros-humble-tf2-ros \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joy \
    ros-humble-teleop-twist-joy \
    ros-humble-cv-bridge \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-nav2-map-server \
    ros-humble-slam-toolbox \
    ros-humble-nav2-common \
    ros-humble-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Installazione librerie Python
RUN pip3 install --no-cache-dir opencv-python pyserial 'numpy<2'

# Creazione struttura workspace ROS2 e copia dei sorgenti
RUN mkdir -p /root/ros2_ws/src
COPY tmp_sources/ /root/ros2_ws/src/

# Clonazione del driver LIDAR LD06 dai sorgenti
RUN cd /root/ros2_ws/src && git clone https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2.git

WORKDIR /root/ros2_ws

# Build dei pacchetti ROS2
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# Creazione entrypoint con configurazione del dominio e del middleware (CycloneDDS)
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'source /opt/ros/humble/setup.bash' >> /entrypoint.sh && \
    echo 'if [ -f "/root/ros2_ws/install/setup.bash" ]; then source /root/ros2_ws/install/setup.bash; fi' >> /entrypoint.sh && \
    echo 'export ROS_DOMAIN_ID=97' >> /entrypoint.sh && \
    echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Integrazione nel .bashrc per sessioni interattive
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "if [ -f \"/root/ros2_ws/install/setup.bash\" ]; then source /root/ros2_ws/install/setup.bash; fi" >> /root/.bashrc \
    && echo "export ROS_DOMAIN_ID=97" >> /root/.bashrc \
    && echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /root/ros2_ws
CMD ["/bin/bash"]
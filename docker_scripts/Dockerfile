# Utilizziamo l'immagine ufficiale ROS2 Humble su base Ubuntu Jammy (compatibile con ARM64 del RPi5)
FROM osrf/ros:humble-ros-base

# Container environment configuration
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    HOME=/root \
    ROS_DISTRO=humble

WORKDIR /root

# Installazione build tools e dipendenze per comunicazione seriale e hardware
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    python3-colcon-common-extensions \
    python3-vcstool \
    python3-serial \
    libserial-dev \
    git \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Creazione struttura workspace ROS2
RUN mkdir -p /root/scooby_real_ws/src
WORKDIR /root/scooby_real_ws

# Installazione dipendenze ROS2 per il robot reale (niente Gazebo qui)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-geometry-msgs \
    ros-humble-std-msgs \
    ros-humble-tf2-ros \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joy \
    ros-humble-teleop-twist-joy \
    && rm -rf /var/lib/apt/lists/*

# Configurazione Entrypoint per il sourcing automatico
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'source /opt/ros/humble/setup.bash' >> /entrypoint.sh && \
    echo 'if [ -f "/root/scooby_real_ws/install/setup.bash" ]; then source /root/scooby_real_ws/install/setup.bash; fi' >> /entrypoint.sh && \
    echo 'export ROS_DOMAIN_ID=97' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Integrazione nel .bashrc per sessioni interattive
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "if [ -f \"/root/scooby_real_ws/install/setup.bash\" ]; then source /root/scooby_real_ws/install/setup.bash; fi" >> /root/.bashrc \
    && echo "export ROS_DOMAIN_ID=97" >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /root/scooby_real_ws
CMD ["/bin/bash"]
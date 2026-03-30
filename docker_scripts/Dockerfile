# Utilizziamo l'immagine ufficiale ROS2 Humble su base Ubuntu Jammy (compatibile con ARM64 del RPi5)
FROM ubuntu:22.04

# Impostazioni ambiente
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    HOME=/root \
    ROS_DISTRO=humble


# Installazione dipendenze di base
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    lsb-release \
    gnupg2 \
    curl \
    build-essential \
    python3-pip \
    python3-serial \
    libserial-dev \
    git \
    udev \
    && locale-gen en_US en_US.UTF-8 && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Installazione colcon e vcstool via pip
RUN pip3 install --no-cache-dir colcon-common-extensions vcstool

# Setup sources ROS2
RUN apt-get update && apt-get install -y curl gnupg2 lsb-release && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | apt-key add - && \
    echo "deb [arch=arm64] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list

# Installazione ROS2 Humble
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-ros-base \
    ros-humble-geometry-msgs \
    ros-humble-std-msgs \
    ros-humble-tf2-ros \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joy \
    ros-humble-teleop-twist-joy \
    ros-humble-cv-bridge \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Container environment configuration
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    HOME=/root \
    ROS_DISTRO=humble

WORKDIR /root


# (già installate sopra)


# Creazione struttura workspace ROS2 e copia dei sorgenti
RUN mkdir -p /root/ros2_ws/src
COPY tmp_sources/ /root/ros2_ws/src/
WORKDIR /root/ros2_ws

# Build dei pacchetti ROS2
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# (già installate sopra)

RUN pip3 install --no-cache-dir opencv-python pyserial 'numpy<2'
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'source /opt/ros/humble/setup.bash' >> /entrypoint.sh && \
    echo 'if [ -f "/root/ros2_ws/install/setup.bash" ]; then source /root/ros2_ws/install/setup.bash; fi' >> /entrypoint.sh && \
    echo 'export ROS_DOMAIN_ID=97' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Integrazione nel .bashrc per sessioni interattive
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "if [ -f \"/root/ros2_ws/install/setup.bash\" ]; then source /root/ros2_ws/install/setup.bash; fi" >> /root/.bashrc \
    && echo "export ROS_DOMAIN_ID=97" >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /root/ros2_ws
CMD ["/bin/bash"]
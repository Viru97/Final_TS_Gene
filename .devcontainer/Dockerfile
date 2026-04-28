FROM osrf/ros:jazzy-desktop-full

# Install essential build tools, git, and your specific ROS 2 dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    ros-jazzy-moveit \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    && rm -rf /var/lib/apt/lists/*

# Fix git tracking issues that happen when volume mounting
RUN git config --global --add safe.directory /workspace

# Automatically source the ROS 2 installation when you open a terminal
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# (Optional) Install your specific Python dependencies globally
# RUN pip3 install --break-system-packages numpy scipy opencv-python
#!/bin/bash

# Ported ROS 2 Pipeline

# Set simulation time (using a hypothetical node name as an example, 
# in ROS 2 parameters are node-specific)
# ros2 param set /some_node use_sim_time true

# Run the GUI node
# Assuming the 'gui' package is migrated and configured for ament_python
ros2 run gui gui_backup.py &

echo "ROS 2 processes started."

while true; do
    read -p "Quit? (y/n): " choice
    if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        pkill -f ros2
        pkill -f rviz2
        break
    else
        echo "Processes will continue running."
    fi
done

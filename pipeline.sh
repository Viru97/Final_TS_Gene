#!/bin/bash

# Open roscore in a new terminal
gnome-terminal -t "roscore" -- bash -c "source devel/setup.bash; roscore"
sleep 2s   

# Set simulation time parameter in a new terminal
gnome-terminal -t "rosparam" -- bash -c "source devel/setup.bash; rosparam set /use_sim_time true"
sleep 1s

# Run the GUI node in a new terminal
gnome-terminal -t "gui" -- bash -c "source devel/setup.bash; rosrun gui gui_backup.py"

# Start a loop to allow user to keep the script open
while true; do
    read -p "Quit? (y/n): " choice
    if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        gnome-terminal -t "end_everything" -- bash -c "ps aux | grep ros | awk '{print \$2}' | xargs kill -9; ps aux | grep rviz | awk '{print \$2}' | xargs kill -9; exec bash"
        break
    else
        echo "Processes will continue running."
    fi
done

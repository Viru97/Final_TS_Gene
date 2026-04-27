'roslaunch panda_gazebo start_workscene.launch' for drilling world launch.
'roslaunch panda_gazebo start_workscene_welding.launch' for welding launch

rosrun panda_gazebo modify_geometry.py
rosrun panda_gazebo randomize_workpiece_position.py
rosrun panda_gazebo randomize_hole_position.py
rosrun panda_gazebo randomize_welding_line.py
rosrun panda_gazebo randomize_hand_position.py


roslaunch panda_gazebo put_robot_in_world.launch load_gripper:=false gripper:=drill/(welding)

rosrun panda_gazebo ee_location.py


moveit control code:
'rosrun pick_and_place pick_and_place_opencv' for drilling
'rosrun pick_and_place pick_and_place_welding' for welding.

NB: modify_geometry shall be done at first.


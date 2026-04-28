cmake_minimum_required(VERSION 3.8)
project(panda_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)

find_package(builtin_interfaces REQUIRED)
find_package(control_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BoundingRegion.msg"
  "msg/JointLimits.msg"
  "srv/AddBox.srv"
  "srv/AddPlane.srv"
  "srv/GetControlledJoints.srv"
  "srv/GetEe.srv"
  "srv/GetEePose.srv"
  "srv/GetEePoseJointConfig.srv"
  "srv/GetEeRpy.srv"
  "srv/GetMoveItControlledJoints.srv"
  "srv/GetRandomEePose.srv"
  "srv/GetRandomJointPositions.srv"
  "srv/LockJoints.srv"
  "srv/SetEe.srv"
  "srv/SetEePose.srv"
  "srv/SetGripperWidth.srv"
  "srv/SetJointCommands.srv"
  "srv/SetJointEfforts.srv"
  "srv/SetJointPositions.srv"
  "action/FollowJointTrajectory.action"
  DEPENDENCIES std_msgs geometry_msgs trajectory_msgs control_msgs builtin_interfaces
)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    nodes/panda_control_server.py
    nodes/panda_moveit_server.py
    nodes/panda_moveit_server_welding.py
    scripts/set_logging_level.py
    scripts/joint_positions_dynamic_reconfigure_server.py
    scripts/joint_efforts_dynamic_reconfigure_server.py
    src/configure_geometry.py
    src/configure_workpiece_position.py
    src/ee_location_backup.py
    src/ee_location_drilling.py
    src/ee_location_welding.py
    src/get_model_info.py
    src/initialize_hand_position.py
    src/initialize_hole_position.py
    src/initialize_welding_line.py
    src/matrix_transform_to_world.py
    src/modify_geometry.py
    src/plot.py
    src/plot_generator.py
    src/randomize_hand_position.py
    src/randomize_hole_position.py
    src/randomize_welding_line.py
    src/randomize_workpiece_position.py
    src/respawn_safety_zones.py
    src/safety_violation_sign.py
    src/set_holes.py
  DESTINATION lib/${PROJECT_NAME}
)

# Legacy ROS1 Gazebo Classic plugin (disabled until ported to GZ + rclcpp).
# add_library(${PROJECT_NAME} src/panda_joint_locker_world_plugin.cpp)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

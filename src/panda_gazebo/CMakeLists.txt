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

# Legacy ROS1 Gazebo Classic plugin (disabled until ported to GZ + rclcpp).
# add_library(${PROJECT_NAME} src/panda_joint_locker_world_plugin.cpp)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

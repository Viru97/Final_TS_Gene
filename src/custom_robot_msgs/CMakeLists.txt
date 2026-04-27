cmake_minimum_required(VERSION 3.8)
project(custom_robot_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# List all your .msg files here
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BoolHeadered.msg"
  "msg/Buffer.msg"
  "msg/Capsule.msg"
  "msg/CapsuleArray.msg"
  "msg/Cylinder.msg"
  "msg/CylinderArray.msg"
  "msg/DoubleHeadered.msg"
  "msg/Motion.msg"
  "msg/Polycapsule.msg"
  "msg/PolycapsuleArray.msg"
  "msg/Positions.msg"
  "msg/PositionsHeadered.msg"
  "msg/PrevStepInfos.msg"
  "msg/Segment.msg"
  "msg/StartGoalCapsuleArray.msg"
  "msg/StartGoalMotion.msg"
  "msg/Visualization.msg"
  DEPENDENCIES std_msgs geometry_msgs
)

ament_package()
cmake_minimum_required(VERSION 3.5)
project(pick_and_place)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)

add_executable(pick_and_place_opencv src/pick_and_place_opencv.cpp)
target_include_directories(pick_and_place_opencv PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(pick_and_place_opencv
  rclcpp
  moveit_ros_planning_interface
  tf2_ros
  tf2_eigen
  tf2_geometry_msgs
  geometry_msgs
  std_msgs
  trajectory_msgs
)

add_executable(pick_and_place_welding src/pick_and_place_welding.cpp)
ament_target_dependencies(pick_and_place_welding
  rclcpp
  moveit_ros_planning_interface
  tf2_ros
  tf2_eigen
  tf2_geometry_msgs
  geometry_msgs
  std_msgs
  trajectory_msgs
)

install(TARGETS
  pick_and_place_opencv
  pick_and_place_welding
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

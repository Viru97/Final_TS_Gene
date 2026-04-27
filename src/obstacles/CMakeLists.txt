cmake_minimum_required(VERSION 3.8)
project(obstacles)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -std=c++17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(custom_robot_msgs REQUIRED)

include_directories(includes)

# Install simulation assets (Gazebo models, worlds, animations, launch files)
install(
  DIRECTORY animations launch models worlds
  DESTINATION share/${PROJECT_NAME}
)

# ==============================================================================
# --- WE WILL UNCOMMENT THESE LATER ONCE WE MIGRATE THE C++ CODE TO RCLCPP ---
# ==============================================================================

# add_executable(stick src/stick.cc)
# ament_target_dependencies(stick rclcpp std_msgs geometry_msgs visualization_msgs tf2 tf2_ros tf2_geometry_msgs custom_robot_msgs)
# install(TARGETS stick DESTINATION lib/${PROJECT_NAME})

# add_executable(cv_model src/cv_model.cc)
# ament_target_dependencies(cv_model rclcpp std_msgs geometry_msgs visualization_msgs tf2 tf2_ros tf2_geometry_msgs custom_robot_msgs)
# install(TARGETS cv_model DESTINATION lib/${PROJECT_NAME})

# add_executable(kf_model src/kf_model.cc)
# ament_target_dependencies(kf_model rclcpp std_msgs geometry_msgs visualization_msgs tf2 tf2_ros tf2_geometry_msgs custom_robot_msgs)
# install(TARGETS kf_model DESTINATION lib/${PROJECT_NAME})

# add_executable(motion_capture src/motion_capture.cc)
# ament_target_dependencies(motion_capture rclcpp std_msgs geometry_msgs visualization_msgs tf2 tf2_ros tf2_geometry_msgs custom_robot_msgs)
# install(TARGETS motion_capture DESTINATION lib/${PROJECT_NAME})

ament_package()
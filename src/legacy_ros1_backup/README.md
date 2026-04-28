# Legacy ROS 1 Backup

This folder contains ROS 1-era sources that were moved out of active package trees
so the workspace can remain ROS 2-only and build cleanly with `colcon`.

## Why these files were moved

These files still relied on ROS 1 APIs such as:
- `#include <ros/ros.h>`
- `ros::init(...)`
- `ros::NodeHandle`
- `ros::AsyncSpinner`

Keeping them in active source paths created migration ambiguity and can cause
future compile/runtime conflicts.

## Current status

- Active workspace packages are ROS 2 buildable.
- Legacy files are preserved here for reference and staged porting.

## Contents

- `pick_and_place/`
  - `own_pick_place_V4.cpp`
  - `own_pick_place_VJZL.cpp`
  - `pick_and_place_opencv_orginal.cpp`
  - `pick_and_place_opencv_working.cpp`
  - `pick_and_place_opencv_drill_prg_bck.cpp`
  - `welding_cpp _old.cpp`

- `obstacles/`
  - `motion_capture.cc`
  - `cv_sphere.cc`
  - `motion_capture.h`

- `panda_gazebo/`
  - `panda_joint_locker_world_plugin.cpp`

## How to port a file back into active source

1. Replace ROS 1 node lifecycle APIs with `rclcpp`/ROS 2 equivalents.
2. Replace ROS 1 logging macros with `RCLCPP_*`.
3. Update service/action patterns to ROS 2 clients/servers.
4. Update any MoveIt 1-specific APIs to MoveIt 2 APIs where applicable.
5. Re-add the file to its package `CMakeLists.txt` only after it compiles.
6. Validate with:
   - `colcon build --symlink-install`
   - package-level runtime smoke test.

## Policy

Until a file is fully ported and validated, keep it in this backup folder and do
not include it in active build targets.

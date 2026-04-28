#include <cmath>
#include <memory>
#include <vector>

#include <geometry_msgs/msg/pose.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int32.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

static constexpr double kTau = 2.0 * M_PI;

void hover_pose(moveit::planning_interface::MoveGroupInterface &move_group, double x, double y, double z) {
  geometry_msgs::msg::Pose target_pose;
  tf2::Quaternion orientation;
  orientation.setRPY(-kTau / 2.0, 0.0, 0.0);
  target_pose.orientation = tf2::toMsg(orientation);
  target_pose.position.x = x;
  target_pose.position.y = y;
  target_pose.position.z = z;
  move_group.setPoseTarget(target_pose);
  move_group.move();
}

void init_pose(moveit::planning_interface::MoveGroupInterface &move_group) {
  auto current_state = move_group.getCurrentState(2.0);
  if (!current_state) return;
  const auto *jmg = current_state->getJointModelGroup("panda_arm");
  std::vector<double> joints;
  current_state->copyJointGroupPositions(jmg, joints);
  if (joints.size() < 7) return;
  joints[0] = 0.0;
  joints[1] = -kTau / 8.0;
  joints[2] = 0.0;
  joints[3] = -3.0 * kTau / 8.0;
  joints[4] = 0.0;
  joints[5] = kTau / 4.0 + 0.03;
  joints[6] = kTau / 8.0;
  move_group.setJointValueTarget(joints);
  move_group.move();
}

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("pick_and_place_welding");
  auto pose_state_pub = node->create_publisher<std_msgs::msg::Int32>("pose_state", 10);

  moveit::planning_interface::MoveGroupInterface move_group(node, "panda_arm");
  move_group.setPlannerId("RRTConnect");
  move_group.setPlanningTime(5.0);

  const std::array<double, 3> start = {0.55, -0.10, 0.25};
  const std::array<double, 3> end = {0.65, 0.10, 0.25};

  std_msgs::msg::Int32 state;
  state.data = 1;
  pose_state_pub->publish(state);
  hover_pose(move_group, start[0], start[1], start[2]);
  state.data = 2;
  pose_state_pub->publish(state);
  hover_pose(move_group, end[0], end[1], end[2]);
  state.data = 3;
  pose_state_pub->publish(state);
  init_pose(move_group);

  rclcpp::shutdown();
  return 0;
}

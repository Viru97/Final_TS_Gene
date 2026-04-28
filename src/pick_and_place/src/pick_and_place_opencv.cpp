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
  auto node = rclcpp::Node::make_shared("pick_and_place_opencv");
  auto pose_state_pub = node->create_publisher<std_msgs::msg::Int32>("pose_state", 10);

  moveit::planning_interface::MoveGroupInterface group_arm(node, "panda_arm");
  group_arm.setPlannerId("RRTConnect");
  group_arm.setPlanningTime(5.0);

  // Parameterized fallback waypoints (removes hard dependency on gazebo_msgs service APIs)
  const std::vector<std::array<double, 3>> holes = {
      {0.60, -0.10, 0.20}, {0.60, 0.00, 0.20}, {0.60, 0.10, 0.20}};

  std_msgs::msg::Int32 state;
  int i = 1;
  for (const auto &h : holes) {
    state.data = i++;
    pose_state_pub->publish(state);
    hover_pose(group_arm, h[0], h[1], h[2] + 0.13);
  }
  state.data = 4;
  pose_state_pub->publish(state);
  init_pose(group_arm);

  rclcpp::shutdown();
  return 0;
}

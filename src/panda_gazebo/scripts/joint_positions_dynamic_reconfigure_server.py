#!/usr/bin/env python3
"""Small node that publishes Panda arm joint positions and gripper width commands."""

import rclpy
from franka_msgs.action import GripperCommand
from rclpy.action import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

from panda_gazebo.common.helpers import wait_for_message

ARM_TOPIC = "/panda_arm_joint_position_controller/command"
JOINT_STATES_TOPIC = "joint_states"
GRIPPER_ACTION_NAME = "franka_gripper/gripper_action"


class JointPositionsDynamicReconfigureServer(Node):
    """Node that publishes joint position commands and optional gripper commands."""

    def __init__(self):
        super().__init__("joint_positions_reconfig_server")
        self.get_logger().info("Starting ROS2 joint positions helper node")

        self.arm_pub = self.create_publisher(Float64MultiArray, ARM_TOPIC, 10)
        self.gripper_client = ActionClient(self, GripperCommand, GRIPPER_ACTION_NAME)
        self.gripper_connected = self.gripper_client.wait_for_server(timeout_sec=5.0)

        self._init_joint_state_timer = self.create_timer(0.5, self._initialize_from_joint_states)
        self._initialized = False

    def _initialize_from_joint_states(self):
        if self._initialized:
            return
        try:
            joint_states = wait_for_message(self, JOINT_STATES_TOPIC, JointState, timeout_sec=1.0)
        except TimeoutError:
            self.get_logger().warn("Waiting for initial joint states...")
            return

        if not joint_states.position:
            self.get_logger().warn("Received empty joint state positions")
            return

        msg = Float64MultiArray()
        msg.data = list(joint_states.position[:7])
        self.arm_pub.publish(msg)
        self._initialized = True
        self.get_logger().info("Initial joint position command published")

    def publish_joint_positions(self, positions):
        msg = Float64MultiArray()
        msg.data = list(positions[:7])
        self.arm_pub.publish(msg)

    def send_gripper_command(self, width, max_effort=0.0):
        if not self.gripper_connected:
            self.get_logger().warn("Gripper action server is unavailable")
            return False

        goal = GripperCommand.Goal()
        goal.command.position = float(width) / 2.0
        goal.command.max_effort = float(max_effort)
        send_goal_future = self.gripper_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()
        return goal_handle is not None and goal_handle.accepted


def main(args=None):
    rclpy.init(args=args)
    node = JointPositionsDynamicReconfigureServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

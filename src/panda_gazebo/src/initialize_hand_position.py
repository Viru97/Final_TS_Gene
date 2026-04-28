#!/usr/bin/env python3
"""Native ROS2 placeholder for legacy script 'initialize_hand_position.py'."""

import rclpy
from rclpy.node import Node


class LegacyScriptNode(Node):
    def __init__(self):
        super().__init__("initialize_hand_position")
        self.get_logger().warning(
            "Script 'initialize_hand_position.py' was a legacy ROS1/shim implementation and now requires a dedicated ROS2 rewrite."
        )


def main(args=None):
    rclpy.init(args=args)
    node = LegacyScriptNode()
    try:
        rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

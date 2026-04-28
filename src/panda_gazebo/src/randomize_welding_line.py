#!/usr/bin/env python3
"""Native ROS2 placeholder for legacy script 'randomize_welding_line.py'."""

import rclpy
from rclpy.node import Node


class LegacyScriptNode(Node):
    def __init__(self):
        super().__init__("randomize_welding_line")
        self.get_logger().warning(
            "Script 'randomize_welding_line.py' was a legacy ROS1/shim implementation and now requires a dedicated ROS2 rewrite."
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

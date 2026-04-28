#!/usr/bin/env python3
"""Set Gazebo logger level using ROS 2 service client."""

import argparse
import sys

import rclpy
from gazebo_msgs.srv import SetLoggerLevel
from rclpy.node import Node


class LoggerLevelClient(Node):
    def __init__(self):
        super().__init__("set_logger_level")
        self.client = self.create_client(SetLoggerLevel, "/gazebo/set_logger_level")

    def set_level(self, logger_name: str, level: str) -> int:
        if not self.client.wait_for_service(timeout_sec=10.0):
            self.get_logger().error("Service /gazebo/set_logger_level not available")
            return 1

        req = SetLoggerLevel.Request()
        req.logger = logger_name
        req.level = level

        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        result = future.result()
        if result is None:
            self.get_logger().error("Service call failed")
            return 1

        self.get_logger().info(f"Set logger '{logger_name}' level to '{level}'")
        return 0


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("logger", help="Logger name")
    parser.add_argument("level", help="Logger level")
    return parser.parse_args(argv)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)

    rclpy.init(args=None)
    node = LoggerLevelClient()
    try:
        return node.set_level(args.logger, args.level)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())

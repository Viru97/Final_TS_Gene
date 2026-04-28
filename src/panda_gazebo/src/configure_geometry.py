#!/usr/bin/env python3

import sys

import rclpy
from rclpy.node import Node


class GeometryConfigurator(Node):
    def __init__(self):
        super().__init__('configure_geometry')

    def run(self, length, width):
        self.get_logger().info(
            f"Requested workpiece geometry update: length={length:.3f}, width={width:.3f}"
        )
        self.get_logger().warning(
            'Model geometry mutation is environment-specific and must be implemented for your model source path.'
        )
        return 0


def main(args=None):
    argv = sys.argv[1:]
    if len(argv) != 2:
        print('Usage: configure_geometry.py <length> <width>')
        raise SystemExit(2)

    rclpy.init(args=args)
    node = GeometryConfigurator()
    try:
        raise SystemExit(node.run(float(argv[0]), float(argv[1])))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

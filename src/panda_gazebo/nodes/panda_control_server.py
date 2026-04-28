#!/usr/bin/env python3
"""This node sets up services/actions for controlling the Panda robot."""

import rclpy

from panda_gazebo.core.control_server import PandaControlServer


def main(args=None):
    rclpy.init(args=args)
    control_server = PandaControlServer()
    try:
        rclpy.spin(control_server)
    finally:
        control_server.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

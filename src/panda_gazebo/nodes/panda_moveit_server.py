#!/usr/bin/env python3
"""Node entrypoint for Panda MoveIt planner services."""

import rclpy

from panda_gazebo.core.moveit_server import PandaMoveItPlannerServer


def main(args=None):
    rclpy.init(args=args)
    node = PandaMoveItPlannerServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

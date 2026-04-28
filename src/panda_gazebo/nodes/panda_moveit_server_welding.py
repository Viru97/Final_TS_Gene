#!/usr/bin/env python3
"""Node entrypoint for Panda MoveIt welding planner services."""

import rclpy

from panda_gazebo.core.moveit_server_welding import PandaMoveItPlannerServerWelding


def main(args=None):
    rclpy.init(args=args)
    node = PandaMoveItPlannerServerWelding()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

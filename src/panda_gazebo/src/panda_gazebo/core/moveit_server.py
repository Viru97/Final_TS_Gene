#!/usr/bin/env python3
"""Native ROS2 minimal server placeholder after ROS1 shim removal."""

from rclpy.node import Node


class PandaMoveItPlannerServer(Node):
    def __init__(self, *args, **kwargs):
        del args, kwargs
        super().__init__("panda_moveit_planner_server")
        self.get_logger().warning(
            "Legacy MoveIt server logic was shim-based and needs full native MoveIt2 reimplementation."
        )

#!/usr/bin/env python3
"""ROS2-native welding variant of planner services."""

from panda_gazebo.core.moveit_server import PandaMoveItPlannerServer


class PandaMoveItPlannerServerWelding(PandaMoveItPlannerServer):
    def __init__(self):
        super().__init__()
        self._ee_name = 'panda_link8'
        self.get_logger().info('Welding planner profile active')

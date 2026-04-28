#!/usr/bin/env python3

import random

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class HoleRandomizer(Node):
    def __init__(self):
        super().__init__('randomize_hole_position')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def _set_hole(self, name, x, y, z):
        msg = ModelState()
        msg.model_name = name
        msg.pose = Pose()
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.pose.orientation.w = 1.0
        req = SetModelState.Request()
        req.model_state = msg
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        return fut.result() is not None

    def run(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/set_model_state unavailable')
            return 1

        cx = random.uniform(0.55, 0.65)
        cy = random.uniform(-0.15, 0.15)
        z = 0.205
        ok = True
        ok &= self._set_hole('hole_1', cx - 0.03, cy, z)
        ok &= self._set_hole('hole_2', cx, cy, z)
        ok &= self._set_hole('hole_3', cx + 0.03, cy, z)

        if not ok:
            self.get_logger().error('Failed to randomize one or more holes')
            return 1
        self.get_logger().info('Hole positions randomized')
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = HoleRandomizer()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import random

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class HandRandomizer(Node):
    def __init__(self):
        super().__init__('randomize_hand_position')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def _set(self, name, x, y, z=0.205):
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
        cy = random.uniform(-0.15, 0.15)
        ok = self._set('hand_1', 0.45, cy - 0.15) and self._set('hand_2', 0.45, cy + 0.15)
        if ok:
            self.get_logger().info('Hand positions randomized')
            return 0
        self.get_logger().error('Failed to randomize hand positions')
        return 1


def main(args=None):
    rclpy.init(args=args)
    node = HandRandomizer()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

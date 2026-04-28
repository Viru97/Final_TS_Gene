#!/usr/bin/env python3

import random

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class WeldingLineRandomizer(Node):
    def __init__(self):
        super().__init__('randomize_welding_line')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def run(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/set_model_state unavailable')
            return 1

        msg = ModelState()
        msg.model_name = 'welding_line'
        msg.pose = Pose()
        msg.pose.position.x = random.uniform(0.52, 0.68)
        msg.pose.position.y = random.uniform(-0.18, 0.18)
        msg.pose.position.z = 0.205
        msg.pose.orientation.w = 1.0
        req = SetModelState.Request()
        req.model_state = msg

        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        if fut.result() is None:
            self.get_logger().error('Failed to randomize welding line position')
            return 1
        self.get_logger().info('Welding line position randomized')
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = WeldingLineRandomizer()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import random

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class WorkpieceRandomizer(Node):
    def __init__(self):
        super().__init__('randomize_workpiece_position')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def run(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/set_model_state unavailable')
            return 1

        msg = ModelState()
        msg.model_name = 'workpiece'
        msg.pose = Pose()
        msg.pose.position.x = random.uniform(0.5, 0.7)
        msg.pose.position.y = random.uniform(-0.3, 0.3)
        msg.pose.position.z = 0.205
        msg.pose.orientation.w = 1.0

        req = SetModelState.Request()
        req.model_state = msg
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        if fut.result() is None:
            self.get_logger().error('Failed to randomize workpiece position')
            return 1
        self.get_logger().info('Workpiece position randomized')
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = WorkpieceRandomizer()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

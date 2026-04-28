#!/usr/bin/env python3

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class WeldingLineInitializer(Node):
    def __init__(self):
        super().__init__('initialize_welding_line')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def run(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/set_model_state unavailable')
            return 1

        msg = ModelState()
        msg.model_name = 'welding_line'
        msg.pose = Pose()
        msg.pose.position.x = 0.60
        msg.pose.position.y = 0.0
        msg.pose.position.z = 0.205
        msg.pose.orientation.w = 1.0
        req = SetModelState.Request()
        req.model_state = msg
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        if fut.result() is None:
            self.get_logger().error('Failed to initialize welding line position')
            return 1
        self.get_logger().info('Welding line position initialized')
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = WeldingLineInitializer()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

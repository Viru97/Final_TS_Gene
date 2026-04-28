#!/usr/bin/env python3

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node
from std_msgs.msg import Int32


class SafetyViolationSign(Node):
    def __init__(self):
        super().__init__('safety_violation_sign')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')
        self.sub = self.create_subscription(Int32, 'safety_violation', self.cb, 10)

    def _set_clone(self, safe):
        msg = ModelState()
        msg.model_name = 'workpiece_clone'
        msg.pose = Pose()
        if safe:
            msg.pose.position.x, msg.pose.position.y, msg.pose.position.z = (0.0, 0.0, -5.0)
        else:
            msg.pose.position.x, msg.pose.position.y, msg.pose.position.z = (0.6, 0.0, 0.205)
        msg.pose.orientation.w = 1.0
        req = SetModelState.Request()
        req.model_state = msg
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)

    def cb(self, msg):
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('/gazebo/set_model_state unavailable')
            return
        self._set_clone(msg.data != 0)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyViolationSign()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class SetHoles(Node):
    def __init__(self):
        super().__init__('set_holes')
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
        ok = True
        ok &= self._set('hole_1', 0.57, -0.05)
        ok &= self._set('hole_2', 0.60, 0.00)
        ok &= self._set('hole_3', 0.63, 0.05)
        if ok:
            self.get_logger().info('Hole positions set')
            return 0
        self.get_logger().error('Failed to set one or more holes')
        return 1


def main(args=None):
    rclpy.init(args=args)
    node = SetHoles()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointStatePlot(Node):
    def __init__(self):
        super().__init__('plot')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self._cb, 10
        )
        self._count = 0
        self.get_logger().info("Listening on '/joint_states'")

    def _cb(self, msg):
        self._count += 1
        if self._count % 20 == 0 and msg.name:
            self.get_logger().info(f'joint sample: {msg.name[0]}={msg.position[0]:.4f}')


def main(args=None):
    rclpy.init(args=args)
    node = JointStatePlot()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

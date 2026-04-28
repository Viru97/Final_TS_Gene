#!/usr/bin/env python3

import sys

import rclpy
from gazebo_msgs.srv import GetModelState
from rclpy.node import Node


class ModelInfo(Node):
    def __init__(self):
        super().__init__('get_model_info')
        self.client = self.create_client(GetModelState, '/gazebo/get_model_state')

    def run(self, model_name):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/get_model_state unavailable')
            return 1
        req = GetModelState.Request()
        req.model_name = model_name
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        resp = fut.result()
        if resp is None:
            self.get_logger().error('Failed to get model state')
            return 1
        p = resp.pose.position
        self.get_logger().info(f'{model_name}: x={p.x:.4f}, y={p.y:.4f}, z={p.z:.4f}')
        return 0


def main(args=None):
    model_name = sys.argv[1] if len(sys.argv) > 1 else 'workpiece'
    rclpy.init(args=args)
    node = ModelInfo()
    try:
        raise SystemExit(node.run(model_name))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

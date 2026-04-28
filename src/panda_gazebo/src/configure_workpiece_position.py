#!/usr/bin/env python3

import math
import sys

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose, Quaternion
from rclpy.node import Node
from tf_transformations import quaternion_from_euler


class ConfigureWorkpiecePosition(Node):
    def __init__(self):
        super().__init__('configure_workpiece_position')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    @staticmethod
    def find_coordinates(position_index: int):
        x_bounds = (0.5, 0.7)
        y_bounds = (-0.3, 0.3)
        rows, cols = 3, 3
        row = max(0, min(rows - 1, (position_index - 1) // cols))
        col = max(0, min(cols - 1, (position_index - 1) % cols))
        x_step = (x_bounds[1] - x_bounds[0]) / (cols - 1)
        y_step = (y_bounds[1] - y_bounds[0]) / (rows - 1)
        return x_bounds[0] + col * x_step, y_bounds[0] + row * y_step

    def run(self, position_index: int, yaw_rad: float):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/gazebo/set_model_state unavailable')
            return 1

        x, y = self.find_coordinates(position_index)
        qx, qy, qz, qw = quaternion_from_euler(0.0, 0.0, yaw_rad)

        model_state = ModelState()
        model_state.model_name = 'workpiece'
        model_state.pose = Pose()
        model_state.pose.position.x = float(x)
        model_state.pose.position.y = float(y)
        model_state.pose.position.z = 0.205
        model_state.pose.orientation = Quaternion(x=qx, y=qy, z=qz, w=qw)

        req = SetModelState.Request()
        req.model_state = model_state
        fut = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        if fut.result() is None:
            self.get_logger().error('Failed to configure workpiece position')
            return 1

        self.get_logger().info(f'Configured workpiece at x={x:.3f}, y={y:.3f}, yaw={yaw_rad:.3f}')
        return 0


def main(args=None):
    argv = sys.argv[1:]
    if len(argv) != 2:
        print('Usage: configure_workpiece_position.py <position_index> <yaw_rad>')
        raise SystemExit(2)

    rclpy.init(args=args)
    node = ConfigureWorkpiecePosition()
    try:
        raise SystemExit(node.run(int(argv[0]), float(argv[1])))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

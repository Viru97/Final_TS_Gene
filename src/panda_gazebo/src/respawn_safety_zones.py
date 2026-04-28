#!/usr/bin/env python3

import rclpy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Pose
from rclpy.node import Node


class SafetyZonesRespawner(Node):
    def __init__(self):
        super().__init__('respawn_safety_zones')
        self.client = self.create_client(SetModelState, '/gazebo/set_model_state')

    def _set(self, name, x, y, z):
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
        specs = [
            ('safety_zone_1', 0.45, -0.25, 0.02),
            ('safety_zone_2', 0.45, 0.25, 0.02),
        ]
        successes = 0
        for name, x, y, z in specs:
            if self._set(name, x, y, z):
                successes += 1
            else:
                self.get_logger().warning(f'Could not set model state for "{name}"')
        if successes == 0:
            self.get_logger().error('No safety-zone models could be respawned')
            return 1
        self.get_logger().info(f'Respawned {successes}/{len(specs)} safety-zone models')
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = SafetyZonesRespawner()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

"""Minimal actionlib-like shim for manual tests, backed by rclpy ActionClient."""

import rclpy
from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient


class SimpleActionClient:
    def __init__(self, name, action_type, node=None):
        if node is None:
            from panda_gazebo.common import rospy_shim as ros

            node = ros.init_node("actionlib_shim_client")
        self._node = node
        self._client = ActionClient(node, action_type, name)
        self._goal_handle = None
        self._result = None

    def wait_for_server(self, timeout=None):
        timeout_sec = float(timeout.nanoseconds) / 1e9 if hasattr(timeout, "nanoseconds") else float(timeout) if timeout is not None else 5.0
        return self._client.wait_for_server(timeout_sec=timeout_sec)

    def send_goal(self, goal, feedback_cb=None):
        fut = self._client.send_goal_async(goal, feedback_callback=feedback_cb)
        rclpy.spin_until_future_complete(self._node, fut)
        self._goal_handle = fut.result()
        return self._goal_handle

    def wait_for_result(self, timeout=None):
        if self._goal_handle is None:
            return False
        fut = self._goal_handle.get_result_async()
        timeout_sec = float(timeout.nanoseconds) / 1e9 if hasattr(timeout, "nanoseconds") else float(timeout) if timeout is not None else None
        rclpy.spin_until_future_complete(self._node, fut, timeout_sec=timeout_sec)
        if not fut.done():
            return False
        self._result = fut.result().result
        return True

    def get_result(self):
        return self._result

    def cancel_goal(self):
        if self._goal_handle is not None:
            fut = self._goal_handle.cancel_goal_async()
            rclpy.spin_until_future_complete(self._node, fut)

    def get_state(self):
        if self._goal_handle is None:
            return GoalStatus.STATUS_UNKNOWN
        return self._goal_handle.status

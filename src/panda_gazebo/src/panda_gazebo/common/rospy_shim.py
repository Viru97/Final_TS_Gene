"""Minimal rospy-like shim backed by rclpy for legacy Panda Gazebo modules."""

from __future__ import annotations

import time
from dataclasses import dataclass

import rclpy
from rclpy.duration import Duration as _Duration
from rclpy.time import Time as _Time

from panda_gazebo.common.helpers import wait_for_message as _wait_for_message

_NODE = None
_WARNED = set()


class ROSException(Exception):
    pass


class ROSInterruptException(Exception):
    pass


class ServiceException(Exception):
    pass


def set_node(node):
    global _NODE
    _NODE = node


def init_node(name, anonymous=False):
    del anonymous
    global _NODE
    if not rclpy.ok():
        rclpy.init(args=None)
    if _NODE is None:
        from rclpy.node import Node

        _NODE = Node(name)
    return _NODE


def _require_node():
    if _NODE is None:
        raise RuntimeError("rospy_shim node is not set")
    return _NODE


def logdebug(msg):
    _require_node().get_logger().debug(str(msg))


def loginfo(msg):
    _require_node().get_logger().info(str(msg))


def logwarn(msg):
    _require_node().get_logger().warn(str(msg))


def logwarn_once(msg):
    if msg not in _WARNED:
        _WARNED.add(msg)
        _require_node().get_logger().warn(str(msg))


def logerr(msg):
    _require_node().get_logger().error(str(msg))


def get_name():
    return _require_node().get_name()


def is_shutdown():
    return not rclpy.ok()


def signal_shutdown(reason=""):
    del reason
    if rclpy.ok():
        rclpy.shutdown()


def spin():
    rclpy.spin(_require_node())


def get_param(name, default=None):
    node = _require_node()
    key = name[1:] if name.startswith("~") else name
    if not node.has_parameter(key):
        node.declare_parameter(key, default)
    return node.get_parameter(key).value


def wait_for_message(topic, msg_type, timeout=None):
    timeout_sec = float(timeout) if timeout is not None else 1.0
    try:
        return _wait_for_message(_require_node(), topic, msg_type, timeout_sec=timeout_sec)
    except TimeoutError as exc:
        raise ROSException(str(exc)) from exc


def wait_for_service(name, timeout=None):
    del name
    del timeout
    return True


class _ServiceProxy:
    def __init__(self, name, srv_type):
        self._node = _require_node()
        self._client = self._node.create_client(srv_type, name)

    def __call__(self, request=None):
        if request is None:
            request = self._client.srv_type.Request()
        self._client.wait_for_service(timeout_sec=5.0)
        future = self._client.call_async(request)
        rclpy.spin_until_future_complete(self._node, future)
        result = future.result()
        if result is None:
            raise ServiceException("Service call failed")
        return result


def ServiceProxy(name, srv_type):
    return _ServiceProxy(name, srv_type)


def Publisher(topic, msg_type, queue_size=10):
    return _require_node().create_publisher(msg_type, topic, queue_size)


def Subscriber(topic, msg_type, callback, queue_size=10):
    return _require_node().create_subscription(msg_type, topic, callback, queue_size)


def Service(name, srv_type, callback):
    def _cb(request, _response):
        return callback(request)

    return _require_node().create_service(srv_type, name, _cb)


class Duration:
    def __new__(cls, seconds=0.0):
        return _Duration(seconds=float(seconds))

    @staticmethod
    def from_sec(seconds):
        return _Duration(seconds=float(seconds))


class Time:
    def __new__(cls, seconds=0.0):
        return _Time(seconds=int(seconds), nanoseconds=int((seconds % 1) * 1e9))

    @staticmethod
    def now():
        return _require_node().get_clock().now()


@dataclass
class _Rate:
    hz: float

    def sleep(self):
        if self.hz > 0:
            time.sleep(1.0 / self.hz)


def Rate(hz):
    return _Rate(float(hz))

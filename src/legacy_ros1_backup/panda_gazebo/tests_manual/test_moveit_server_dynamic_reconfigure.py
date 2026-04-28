#!/usr/bin/env python3
"""Node to dynamically reconfigure 'panda_moveit_planner_server' parameters."""

from panda_gazebo.common import rospy_shim as rospy
Server = None  # ROS2: dynamic_reconfigure not supported in manual test

from panda_gazebo.cfg import MoveitServerConfig


def callback(config, level):
    """Dynamic reconfigure callback function.

    Args:
        config (:obj:`dynamic_reconfigure.encoding.Config`): The current dynamic
            reconfigure configuration object.
        level (int): Bitmask that gives information about which parameter has been
            changed.

    Returns:
        :obj:`~dynamic_reconfigure.encoding.Config`: Modified dynamic reconfigure
            configuration object.
    """
    rospy.loginfo(
        (
            "Reconfigure Request: {max_velocity_scaling_factor}, "
            "{max_acceleration_scaling_factor}"
        ).format(**config)
    )
    return config


if __name__ == "__main__":
    rospy.init_node("moveit_server_dynamic_reconfigure_server_test", anonymous=False)

    print("dynamic_reconfigure manual test skipped on ROS2")
    pass

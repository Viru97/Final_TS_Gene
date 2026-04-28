import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource


def generate_launch_description():
    share = get_package_share_directory("panda_gazebo")
    legacy_launch = os.path.join(share, "launch", "start_workscene.launch")

    # Bridge ROS 2 CLI callers to the existing frontend launch description.
    return LaunchDescription(
        [
            IncludeLaunchDescription(AnyLaunchDescriptionSource(legacy_launch)),
        ]
    )

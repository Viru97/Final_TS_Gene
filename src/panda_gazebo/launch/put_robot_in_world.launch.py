import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    share = get_package_share_directory("panda_gazebo")
    legacy_launch = os.path.join(share, "launch", "put_robot_in_world.launch")

    rviz = LaunchConfiguration("rviz")
    moveit = LaunchConfiguration("moveit")
    load_gripper = LaunchConfiguration("load_gripper")
    gripper = LaunchConfiguration("gripper")
    control_type = LaunchConfiguration("control_type")

    return LaunchDescription(
        [
            DeclareLaunchArgument("rviz", default_value="true"),
            DeclareLaunchArgument("moveit", default_value="true"),
            DeclareLaunchArgument("load_gripper", default_value="false"),
            DeclareLaunchArgument("gripper", default_value="drill"),
            DeclareLaunchArgument("control_type", default_value="trajectory"),
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(legacy_launch),
                launch_arguments={
                    "rviz": rviz,
                    "moveit": moveit,
                    "load_gripper": load_gripper,
                    "gripper": gripper,
                    "control_type": control_type,
                }.items(),
            ),
        ]
    )

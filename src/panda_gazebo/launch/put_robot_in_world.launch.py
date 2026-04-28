from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    moveit = LaunchConfiguration("moveit")
    control_type = LaunchConfiguration("control_type")

    return LaunchDescription(
        [
            DeclareLaunchArgument("moveit", default_value="true"),
            DeclareLaunchArgument("load_gripper", default_value="false"),
            DeclareLaunchArgument("gripper", default_value="drill"),
            DeclareLaunchArgument("control_type", default_value="trajectory"),
            Node(
                package='panda_gazebo',
                executable='panda_control_server.py',
                name='panda_control_server',
                output='screen',
                parameters=[
                    {
                        'load_set_joint_commands_service': True,
                        'load_arm_follow_joint_trajectory_action': False,
                        'load_extra_services': True,
                        'load_gripper': True,
                    }
                ],
            ),
            Node(
                condition=IfCondition(moveit),
                package='panda_gazebo',
                executable='panda_moveit_server.py',
                name='panda_moveit_planner_server',
                output='screen',
            ),
            Node(
                package='panda_gazebo',
                executable='set_logging_level.py',
                name='set_logging_level_franka_control',
                output='screen',
                arguments=['--name', 'ros.franka_gazebo.FrankaGripperSim', '--level', 'warn'],
            ),
        ]
    )

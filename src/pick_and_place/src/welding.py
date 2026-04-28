#!/usr/bin/env python3

import sys
from panda_gazebo.common import rospy_shim as ros
import moveit_commander
from geometry_msgs.msg import Pose, Quaternion
from moveit_msgs.msg import RobotTrajectory
from tf.transformations import quaternion_from_euler
import math
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from get_model_info import get_model_dimensions
from matrix_transform_to_world import transform_from_local_to_world
import random
from std_msgs.msg import Float32, String

speed = Float32()
acceleration = Float32()
planning_algorithm = String()

tau = 2 * math.pi

def hoverPose(move_group, x, y, z):
    # Set joint value for the 7th joint to keep it locked
    joint_group_positions = move_group.get_current_joint_values()
    joint_group_positions[6] = 0  # Specify desired joint value here
    move_group.set_joint_value_target(joint_group_positions)
    # We can plan a motion for this group to a desired pose for the end-effector.
    target_pose_hover = Pose()

    # Convert Orientation from RPY to Quaternion
    quaternion = Quaternion(*quaternion_from_euler(-tau/2, 0, 0))

    target_pose_hover.orientation = quaternion
    target_pose_hover.position.x = x
    target_pose_hover.position.y = y
    target_pose_hover.position.z = z
    move_group.set_pose_target(target_pose_hover)
    move_group.go()

def initPose(move_group):
    # Get the current robot state
    current_state = move_group.get_current_state()
    # Get the current joint values for the group
    joint_group_positions = current_state.joint_state.position

    # Set the desired joint positions for the initial pose
    joint_group_positions = [0, -tau / 8, 0, -3 * tau / 8, 0, tau / 4 + 0.03, tau / 8]
    # Set the joint value target
    move_group.set_joint_value_target(joint_group_positions)
    # Set maximum velocity and acceleration scaling factors
    # move_group.set_max_velocity_scaling_factor(0.2)
    # move_group.set_max_acceleration_scaling_factor(0.2)
    # Move the robot to the initial pose
    move_group.go()


def pickPose(move_group, direction, x, y, z):
    # Set joint value for the 7th joint to keep it locked
    joint_group_positions = move_group.get_current_joint_values()
    joint_group_positions[6] = 0  # Specify desired joint value here
    move_group.set_joint_value_target(joint_group_positions)

    move_group.set_start_state_to_current_state()
    # move_group.set_max_velocity_scaling_factor(0.02)
    # move_group.set_max_acceleration_scaling_factor(0.01)

    waypoints = []
    
    target_pose_pick = move_group.get_current_pose().pose
    target_pose_pick.position.x = x
    target_pose_pick.position.y = y
    target_pose_pick.position.z = z
    if direction == "down":
        target_pose_pick.position.z -= 0.0
    elif direction == "up":
        target_pose_pick.position.z += 0.0
    # quaternion = Quaternion(*quaternion_from_euler(-tau/2, 0, 0))

    # target_pose_pick.orientation = quaternion
    waypoints.append(target_pose_pick)

    (plan, fraction) = move_group.compute_cartesian_path(
                                                        waypoints,
                                                        0.01,   # eef_step
                                                        False)    # jump_threshold

    robot_trajectory = RobotTrajectory()
    robot_trajectory.joint_trajectory = plan.joint_trajectory

    # Create a IterativeParabolicTimeParameterization object
    #iptp = IterativeParabolicTimeParameterization()

    # # # Compute TimeStamps
    # # iptp.compute_time_stamps(robot_trajectory)

    # cartesian_plan = RobotTrajectory()
    # robot_trajectory.get_robot_trajectory_msg(cartesian_plan)
    move_group.execute(plan)

def main():

    moveit_commander.roscpp_initialize(sys.argv)
    ros.init_node('own_pick_place_V4', anonymous=True)
    pub_speed = ros.Publisher('speed', Float32, queue_size=10, latch=True)
    pub_acc = ros.Publisher('acceleration', Float32, queue_size=10, latch=True)
    pub_plan = ros.Publisher('planning_algorithm', String, queue_size=10, latch=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "panda_arm"
    group_arm = moveit_commander.MoveGroupCommander(group_name)
    planner_list = [
    "AnytimePathShortening",
    "SBL",
    "EST",
    "LBKPIECE",
    "BKPIECE",
    "KPIECE",
    "RRT",
    "RRTConnect",
    "RRTstar",
    "TRRT",
    "PRM",
    "PRMstar",
    "FMT",
    "BFMT",
    "PDST",
    "STRIDE",
    "BiTRRT",
    "LBTRRT",
    "BiEST",
    "ProjEST",
    "LazyPRM",
    "LazyPRMstar",
    "SPARS",
    "SPARStwo",
    "AITstar",
    "ABITstar",
    "BITstar"
    ]

    planner = random.choice(planner_list)
    ros.logerr(f"Selected Planner: {planner}")

    # available_planners = move_group.get_interface_description().planner_ids
    # ros.logwarn(available_planners)
    # if planner in available_planners:
    group_arm.set_planner_id(planner)
    ros.logerr(f"Planner set to: {planner}")
    # else:
        # ros.logerr(f"Planner {planner} not available. Using default planner.")

    velocity_factor = random.uniform(0.1, 0.5)
    acceleration_factor = random.uniform(0.1, 0.5)
    ros.logerr(f'velocity factor {velocity_factor}')
    ros.logerr(f'acceleration factor {acceleration_factor}')

    group_arm.set_max_velocity_scaling_factor(velocity_factor)
    group_arm.set_max_acceleration_scaling_factor(acceleration_factor)
    acceleration.data = acceleration_factor
    speed.data = velocity_factor
    planning_algorithm.data = planner

    pub_speed.publish(speed)
    pub_acc.publish(acceleration)
    pub_plan.publish(planning_algorithm)


    group_arm.set_planning_time(5.0)

    # Set joint value for the 7th joint to keep it locked
    joint_group_positions = group_arm.get_current_joint_values()
    joint_group_positions[6] = 0  # Specify desired joint value here
    group_arm.set_joint_value_target(joint_group_positions)

    # Get current position from Gazebo
    model_name = "welding_line"
    response=ModelState()
    get_model_state = ros.ServiceProxy('/gazebo/get_model_state', GetModelState)
    response = get_model_state(model_name, "world")
    x, y, z = response.pose.position.x, response.pose.position.y, response.pose.position.z
    yaw=yaw = math.atan2(2 * (response.pose.orientation.w * response.pose.orientation.z), 1 - 2 * (response.pose.orientation.z ** 2))
    
    dimension= get_model_dimensions("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/welding_line/model.sdf")
    length, width, height = dimension
    # ros.loginfo("Length of the welding line: {} {}".format(length,yaw))
    
    # Calculate the start & end position of the line segment
    start_x,start_y,start_z = transform_from_local_to_world((-length/2,0.0,0.0),(x,y,z,0,0,yaw))
    end_x, end_y, end_z = transform_from_local_to_world((length/2,0.0,0.0),(x,y,z,0,0,yaw))
    
    # ros.loginfo("Start position (x, y, z): ({}, {}, {})".format(start_x, start_y, start_z))
    # ros.loginfo("End position (x, y, z): ({}, {}, {})".format(end_x, end_y, end_z))
    
    # Perform welding operation
    hoverPose(group_arm, start_x+0.00, start_y, (start_z + 0.127))
    pickPose(group_arm, "down", start_x+0.00, start_y, (start_z + 0.0))
    hoverPose(group_arm, start_x+0.00+(end_x-start_x)/3, end_y,(end_z + 0.0))

    hoverPose(group_arm, start_x+0.00+(end_x-start_x)*2/3, end_y,(end_z + 0.0))

    hoverPose(group_arm, end_x+0.00, end_y,(end_z + 0.0))
    # num_waypoints = 20
    # for i in range(num_waypoints + 1):  # +1 to include the end point
    #     fraction = i / num_waypoints  # Fractional distance along the line
    #     waypoint_x = start_x + fraction * (end_x - start_x)
    #     waypoint_y = start_y + fraction * (end_y - start_y)
    #     waypoint_z = start_z  # Maintain same height

    #     hoverPose(group_arm, waypoint_x, waypoint_y, waypoint_z)

    pickPose(group_arm, "up", end_x+0.00, end_y,(end_z + 0.127))
    ros.sleep(1.0)  # Delay for 2 seconds
    initPose(group_arm) 
    ros.sleep(3.0)  # Delay for 3 seconds
    ros.logwarn("Round end")

    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()

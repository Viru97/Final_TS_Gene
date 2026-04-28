#!/usr/bin/env python3

import sys
from panda_gazebo.common import rospy_shim as ros
import moveit_commander
from moveit_msgs.msg import RobotTrajectory
from geometry_msgs.msg import Pose, Quaternion
import tf2_ros
from tf.transformations import quaternion_from_euler
import math
import time
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
import random
from std_msgs.msg import Float32, String


speed = Float32()
acceleration = Float32()
planning_algorithm = String()
# The circle constant tau = 2*pi. One tau is one rotation in radians.
tau = 2 * math.pi

# Position, Orientation, Planning, Execution hoverPose
def hoverPose(move_group, x, y, z):
    # move_group.set_max_velocity_scaling_factor(0.1)
    # move_group.set_max_acceleration_scaling_factor(0.1)
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
    # move_group.set_max_velocity_scaling_factor(0.1)
    # move_group.set_max_acceleration_scaling_factor(0.1)
    # Move the robot to the initial pose
    move_group.go()

def pickPose(move_group, direction, x, y, z):
    move_group.set_start_state_to_current_state()
    # move_group.set_max_velocity_scaling_factor(0.005)
    # move_group.set_max_acceleration_scaling_factor(0.005)

    waypoints = []
    
    target_pose_pick = move_group.get_current_pose().pose
    target_pose_pick.position.x = x
    target_pose_pick.position.y = y
    target_pose_pick.position.z = z
    if direction == "down":
        target_pose_pick.position.z -= 0.0
    elif direction == "up":
        target_pose_pick.position.z += 0.15
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
   
    ros.init_node('own_pick_place_V4', anonymous=True)
    pub_speed = ros.Publisher('speed', Float32, queue_size=10, latch=True)
    pub_acc = ros.Publisher('acceleration', Float32, queue_size=10, latch=True)
    pub_plan = ros.Publisher('planning_algorithm', String, queue_size=10, latch=True)

    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "panda_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
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
    "BITstar"]

    planner = random.choice(planner_list)
    ros.logerr(f"Selected Planner: {planner}")

    # available_planners = move_group.get_interface_description().planner_ids
    # ros.logwarn(available_planners)
    # if planner in available_planners:
    move_group.set_planner_id(planner)
    ros.logerr(f"Planner set to: {planner}")
    # else:
        # ros.logerr(f"Planner {planner} not available. Using default planner.")

    velocity_factor = random.uniform(0.1, 0.5)
    acceleration_factor = random.uniform(0.1, 0.5)
    ros.logerr(f'velocity factor {velocity_factor}')
    ros.logerr(f'acceleration factor {acceleration_factor}')

    move_group.set_max_velocity_scaling_factor(velocity_factor)
    move_group.set_max_acceleration_scaling_factor(acceleration_factor)
    acceleration.data = acceleration_factor
    speed.data = velocity_factor
    planning_algorithm.data = planner


    pub_speed.publish(speed)
    pub_acc.publish(acceleration)
    pub_plan.publish(planning_algorithm)

    move_group.set_planning_time(5.0)

    model_names = ["hole_1", "hole_2", "hole_3"]
    for model_name in model_names:
        try:
            response= ModelState()
            response.pose = Pose()
            get_model_state = ros.ServiceProxy('/gazebo/get_model_state', GetModelState)
            response = get_model_state(model_name, "world")
            if model_name == "hole_1":
                hole1_x, hole1_y, hole1_z = response.pose.position.x, response.pose.position.y, response.pose.position.z
            elif model_name == "hole_2":
                hole2_x, hole2_y, hole2_z = response.pose.position.x, response.pose.position.y, response.pose.position.z
            elif model_name == "hole_3":
                hole3_x, hole3_y, hole3_z = response.pose.position.x, response.pose.position.y, response.pose.position.z
        except ros.ServiceException as e:
            print("Service call failed:", e)

    time.sleep(1.0)

    hoverPose(move_group, hole1_x, hole1_y, hole1_z + 0.15)
    pickPose(move_group, "down", hole1_x, hole1_y, hole1_z + 0.0)
    time.sleep(1.0)
    pickPose(move_group, "up", hole1_x, hole1_y, hole1_z)
    initPose(move_group)
    ros.logwarn("round1 end")

    hoverPose(move_group, hole2_x, hole2_y, hole2_z + 0.15)
    pickPose(move_group, "down", hole2_x, hole2_y, hole2_z + 0.0)
    time.sleep(1.0)
    pickPose(move_group, "up", hole2_x, hole2_y, hole2_z)
    initPose(move_group)
    ros.logwarn("round2 end")

    hoverPose(move_group, hole3_x, hole3_y, hole3_z + 0.15)
    pickPose(move_group, "down", hole3_x, hole3_y, hole3_z + 0.0)
    time.sleep(1.0)
    pickPose(move_group, "up",  hole3_x, hole3_y, hole3_z)
    initPose(move_group)
    ros.logwarn("round3 end")
    ros.sleep(1.0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import time
from panda_gazebo.common import rospy_shim as ros
from random import uniform
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from matrix_transform_to_world import transform_from_local_to_world
from get_model_info import get_model_dimensions, get_model_pose, write_pose_to_sdf_file


def randomize_hole_position():
    model_name = "workpiece"
    model_path = "/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/workpiece/model.sdf" 
    workpiece_pose = get_model_pose(model_name)
    workpiece_dimensions = get_model_dimensions(model_path)
    length, width, height = workpiece_dimensions
    
    #Randomize three points in relative cordinate system respect to workpiece
    hole_1_x,hole_1_y,hole_1_z = 10, 0, 0
    hole_2_x,hole_2_y,hole_2_z = 10, 0, 0    
    hole_3_x,hole_3_y,hole_3_z = 10, 0, 0

    local_cordinates_hole_1 = (hole_1_x,hole_1_y,hole_1_z)
    local_cordinates_hole_2 = (hole_2_x,hole_2_y,hole_2_z)
    local_cordinates_hole_3 = (hole_3_x,hole_3_y,hole_3_z)

    world_cordinates_hole_1 =transform_from_local_to_world(local_cordinates_hole_1, workpiece_pose)
    world_cordinates_hole_2 =transform_from_local_to_world(local_cordinates_hole_2, workpiece_pose)
    world_cordinates_hole_3 =transform_from_local_to_world(local_cordinates_hole_3, workpiece_pose)
    ros.loginfo(f"Hole_1_position in world_coordinates: {world_cordinates_hole_1}")
    ros.wait_for_service('/gazebo/set_model_state')
    set_state = ros.ServiceProxy('/gazebo/set_model_state', SetModelState)

    # # SET Holes POSITION # # #
    model_name_hole_1 = "hole_1"  # Replace with your hole model name
    hole_1_state = ModelState()
    hole_1_state.model_name = model_name_hole_1
    hole_1_state.pose = Pose()
    hole_1_state.pose.position.x = world_cordinates_hole_1[0]
    hole_1_state.pose.position.y = world_cordinates_hole_1[1]
    hole_1_state.pose.position.z = world_cordinates_hole_1[2]
    modified=write_pose_to_sdf_file("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/hole_1/model.sdf", hole_1_state.pose)

    model_name_hole_2 = "hole_2"  # Replace with your hole model name
    hole_2_state = ModelState()
    hole_2_state.model_name = model_name_hole_2
    hole_2_state.pose = Pose()
    hole_2_state.pose.position.x = world_cordinates_hole_2[0]
    hole_2_state.pose.position.y = world_cordinates_hole_2[1]
    hole_2_state.pose.position.z = world_cordinates_hole_2[2]
    modified=write_pose_to_sdf_file("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/hole_2/model.sdf", hole_2_state.pose)

    model_name_hole_3 = "hole_3"  # Replace with your hole model name
    hole_3_state = ModelState()
    hole_3_state.model_name = model_name_hole_3
    hole_3_state.pose = Pose()
    hole_3_state.pose.position.x = world_cordinates_hole_3[0]
    hole_3_state.pose.position.y = world_cordinates_hole_3[1]
    hole_3_state.pose.position.z = world_cordinates_hole_3[2]
    modified=write_pose_to_sdf_file("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/hole_3/model.sdf", hole_3_state.pose)

    try:
        set_state(hole_1_state)
        time.sleep(1)  # Add a delay
        set_state(hole_2_state)
        time.sleep(1)  # Add a delay
        set_state(hole_3_state)
        time.sleep(1)  # Add a delay
        ros.loginfo("Holes position intialized.")
    except ros.ServiceException as e:
        ros.logerr("Failed to call Gazebo service: %s", str(e))

if __name__ == '__main__':
    ros.init_node('randomize_holes')
    randomize_hole_position()

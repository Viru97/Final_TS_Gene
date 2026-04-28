#!/usr/bin/env python3
import math
import time
from panda_gazebo.common import rospy_shim as ros
from random import uniform
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Quaternion
from tf.transformations import quaternion_from_euler
from get_model_info import get_model_state, write_pose_to_sdf_file,get_model_dimensions

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)


def randomize_hands_position():
     #Table location end points
    min_x, max_x = 0.5, 0.7  # Adjust the desired range for x position
    min_y, max_y = -0.4, 0.4  # Adjust the desired range for y position
    min_z, max_z = 0.200508, 0.200509  # Adjust the desired range for z position
    ros.wait_for_service('/gazebo/set_model_state')
    set_state = ros.ServiceProxy('/gazebo/set_model_state', SetModelState)
    workpiece_pose = get_model_state("workpiece")
    workpiece_cordinates=(workpiece_pose.position.x,workpiece_pose.position.y,workpiece_pose.position.z)
    workpiece_dimensions = get_model_dimensions("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/workpiece/model.sdf")
    max_dimension= max(workpiece_dimensions[0],workpiece_dimensions[1])

    hand_1_name_model = "hand_1"  # Assign the model to a state
    hand_1_model_state = ModelState()
    hand_1_model_state.model_name = hand_1_name_model
    hand_1_model_state.pose = Pose() 
    while True:       
        hand_1_model_state.pose.position.x = uniform(min_x, max_x)
        hand_1_model_state.pose.position.y = uniform(0, max_y)
        hand_1_model_state.pose.position.z = uniform(min_z, max_z)
        hand_1_cordinates=(hand_1_model_state.pose.position.x,hand_1_model_state.pose.position.y,hand_1_model_state.pose.position.z)
        hand_1_model_state.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, 0))
        
        if calculate_distance(workpiece_cordinates, hand_1_cordinates)>((max_dimension+0.1)*0.7):
            break
    modified=write_pose_to_sdf_file("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/hand_1/model.sdf", hand_1_model_state.pose)    
    
    hand_2_name_model = "hand_2"  # Assign the model to a state
    hand_2_model_state = ModelState()
    hand_2_model_state.model_name = hand_2_name_model
    hand_2_model_state.pose = Pose() 
    while True:       
        hand_2_model_state.pose.position.x = uniform(min_x, max_x)
        hand_2_model_state.pose.position.y = uniform(min_y, 0)
        hand_2_model_state.pose.position.z = uniform(min_z, max_z)
        hand_2_cordinates=(hand_2_model_state.pose.position.x,hand_2_model_state.pose.position.y,hand_2_model_state.pose.position.z)
        hand_2_model_state.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, 0))
        if (calculate_distance(workpiece_cordinates, hand_2_cordinates)>((max_dimension+0.1)*0.7)) and (calculate_distance(hand_1_cordinates, hand_2_cordinates)>0.4):
            break
    modified=write_pose_to_sdf_file("/home/baua/Final_TS_Gene/src/panda_gazebo/resources/models/hand_1/model.sdf", hand_2_model_state.pose)
    
    
    try:
        set_state(hand_1_model_state)
        time.sleep(0.1)  # Add a delay
        ros.loginfo("hand_1 position randomized.") 
        set_state(hand_2_model_state)
        time.sleep(0.1)  # Add a delay
        ros.loginfo("hand_2 position randomized.") 
    except ros.ServiceException as e:
        ros.logerr("Failed to call Gazebo service: %s", str(e))


if __name__ == '__main__':
    ros.init_node('randomize_hands_position')
    randomize_hands_position()
    
    
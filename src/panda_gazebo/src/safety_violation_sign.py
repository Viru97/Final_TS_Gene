#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState

class WorkpiecePositionChanger:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node("safety_violation_position_changer")

        # Set up a subscriber to the safety_violation topic
        rospy.Subscriber("safety_violation", Int32, self.safety_violation_callback)

        # Wait for the 'set_model_state' service to become available
        rospy.wait_for_service('/gazebo/set_model_state')
        self.set_model_state_service = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    def safety_violation_callback(self, msg):
        model_state = ModelState()
        model_state.model_name = 'workpiece_clone'

        # Set a new position based on the safety violation status
        if msg.data == 1:
            # Move the model to a "safe" position when violation occurs
            model_state.pose.position.x = 0.6    # Set your desired "safe" coordinates
            model_state.pose.position.y = 0
            model_state.pose.position.z = 0.1
            # rospy.loginfo("Safety violation detected: moving workpiece_clone to safe position.")
        else:
            # Return to default position when no violation
            model_state.pose.position.x = 0.6  # Set your original/default coordinates
            model_state.pose.position.y = 0.0
            model_state.pose.position.z = -1.0
            # rospy.loginfo("No safety violation: moving workpiece_clone to default position.")

        # Update the model state in Gazebo
        try:
            self.set_model_state_service(model_state)
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")

if __name__ == "__main__":
    WorkpiecePositionChanger()
    rospy.spin()

#!/usr/bin/env python3
import subprocess
import signal
import sys
import time
import rospy
from gazebo_msgs.srv import GetModelState


def run_node(pkg, node_type, args=None, timeout=10):
    command = ['rosrun', pkg, node_type]
    if args:
        command.extend(args)

    while True:
        print(f"Starting node: {node_type} from package: {pkg}")
        
        # Capture both stdout and stderr
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        start_time = time.time()  # Record the start time

        while True:
            # Wait for the process to finish or check the timeout
            if process.poll() is not None:  # Process finished
                stdout, stderr = process.communicate()
                # Check if the process exited successfully (exit code 0)
                if process.returncode == 0:
                    print(f"Node {node_type} ran successfully.")
                    return  # Exit the function if successful
                else:
                    print(f"Node {node_type} failed to run. Error: {stderr.decode()}")
                    break  # Restart the node

            # Check if the process is running for more than the timeout
            if time.time() - start_time > timeout:
                print(f"Node {node_type} did not start within {timeout} seconds. Restarting...")
                process.terminate()  # Terminate the process
                break  # Restart the node

            time.sleep(0.5)  # Add a short sleep to avoid busy waiting


def check_model_exists(model_name, timeout=2):

    rospy.logwarn('checking model')
    """
    Check if the specified model exists in the Gazebo simulation.
    
    Args:
        model_name (str): The name of the model to check.
        timeout (int): The time (in seconds) to wait before timing out.

    Returns:
        bool: True if the model exists, False otherwise.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            rospy.wait_for_service('/gazebo/get_model_state', timeout=1)
            get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            response = get_model_state(model_name, "")
            if response.success:
                rospy.loginfo(f"Model '{model_name}' exists.")
                return True  # Model exists
        except rospy.ROSException:
            # The service may not be available yet; continue checking
            pass
        
        rospy.loginfo(f"Waiting for model '{model_name}' to spawn...")
        time.sleep(1)  # Wait before checking again

    rospy.logerr(f"Model '{model_name}' did not spawn within {timeout} seconds.")
    return False  # Model does not exist within timeout

def randomize_model(model_name, randomize_script):
    rospy.logwarn('will checking model start')

    """Randomize the specified model using the given script."""
    if check_model_exists(model_name):
        run_node('panda_gazebo', randomize_script)
    else:
        rospy.logerr(f"Restarting {randomize_script} due to missing model '{model_name}'.")
        run_node('panda_gazebo', 'modify_geometry.py')  # Restart geometry modification as a fallback


if __name__ == "__main__":
    rospy.init_node('generator_mode')  # Initialize the ROS node

    # Launch the work scene
    subprocess.Popen(['roslaunch', 'panda_gazebo', 'start_workscene.launch', 'gazebo_gui:=false'])    
    # rospy.logwarn('will checking model start')
    time.sleep(1)
    # Modify the geometry
    run_node('panda_gazebo', 'modify_geometry.py')
    time.sleep(1)

    # Randomize the workpiece position
    randomize_model('workpiece', 'randomize_workpiece_position.py')
    time.sleep(1)

    # Randomize the hole position
    randomize_model('workpiece', 'randomize_hole_position.py')
    time.sleep(1)

    # Randomize the hand position
    run_node('panda_gazebo', 'randomize_hand_position.py')
    time.sleep(1)

    # Put the robot in the world
    subprocess.Popen(['roslaunch', 'panda_gazebo', 'put_robot_in_world.launch','gazebo_gui:=false', 'rviz:=false', 'load_gripper:=false', 'gripper:=drill'])
    # Run the drilling process
    # run_node('panda_gazebo', 'ee_location_drilling.py')
    rospy.logwarn('Ready')
    rospy.logwarn('Ready')
    rospy.logwarn('Ready')
    rospy.logwarn('Ready')

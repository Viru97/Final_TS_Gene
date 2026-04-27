#!/usr/bin/env python3
import subprocess
import time
import rclpy
from rclpy.node import Node

node = None


def ros2_run_cmd(package, executable, *args):
    return ["ros2", "run", package, executable, *args]


def ros2_launch_cmd(package, launch_file, *args):
    launch_name = f"{launch_file}.py" if launch_file.endswith(".launch") else launch_file
    return ["ros2", "launch", package, launch_name, *args]


def run_node(pkg, node_type, args=None, timeout=10):
    command = ros2_run_cmd(pkg, node_type, *(args or []))

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
    # Gazebo ROS2 service APIs vary between simulator versions; run the randomizer directly.
    node.get_logger().info(f"Skipping model existence check for '{model_name}' in ROS2 mode")
    return True

def randomize_model(model_name, randomize_script):
    node.get_logger().warning('Checking model before randomization')

    """Randomize the specified model using the given script."""
    if check_model_exists(model_name):
        run_node('panda_gazebo', randomize_script)
    else:
        node.get_logger().error(f"Restarting {randomize_script} due to missing model '{model_name}'.")
        run_node('panda_gazebo', 'modify_geometry.py')  # Restart geometry modification as a fallback


def main(args=None):
    global node

    if not rclpy.ok():
        rclpy.init(args=args)

    node = Node('generator_mode')

    # Launch the work scene
    subprocess.Popen(ros2_launch_cmd('panda_gazebo', 'start_workscene.launch', 'gazebo_gui:=false'))
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
    subprocess.Popen(
        ros2_launch_cmd(
            'panda_gazebo',
            'put_robot_in_world.launch',
            'gazebo_gui:=false',
            'rviz:=false',
            'load_gripper:=false',
            'gripper:=drill',
        )
    )
    # Run the drilling process
    # run_node('panda_gazebo', 'ee_location_drilling.py')
    node.get_logger().warning('Ready')
    node.get_logger().warning('Ready')
    node.get_logger().warning('Ready')
    node.get_logger().warning('Ready')

    if node is not None:
        node.destroy_node()
        node = None
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()

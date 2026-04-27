#include <ros/ros.h>
#include <geometry_msgs/Pose.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/static_transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Transform.h>
#include <tf2/LinearMath/Vector3.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <tf2/convert.h>
#include <tf2/utils.h>
#include <moveit_msgs/GetPositionIK.h>
#include <moveit_msgs/GetPositionFK.h>
#include <moveit_msgs/DisplayTrajectory.h>
#include <moveit_msgs/RobotState.h>
#include <moveit_msgs/RobotTrajectory.h>
#include <moveit_msgs/PlanningScene.h>
#include <moveit_msgs/ExecuteTrajectoryAction.h>
#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/robot_model/robot_model.h>
#include <moveit/kinematic_constraints/utils.h>
#include <moveit/trajectory_processing/iterative_time_parameterization.h>
#include <moveit/robot_state/conversions.h>
#include <moveit_msgs/GetPlanningScene.h>
#include <moveit_msgs/PlanningSceneComponents.h>
#include <gazebo_msgs/GetModelState.h>
#include <gazebo_msgs/ModelState.h>
#include <math.h>
#include "std_msgs/Bool.h"
#include "std_msgs/Int32.h"

const double tau = 2 * M_PI;

void hoverPose(moveit::planning_interface::MoveGroupInterface& move_group, float x, float y, float z)
{ 
  // We can plan a motion for this group to a desired pose for the
  // end-effector.
  geometry_msgs::Pose target_pose_hover;

  //Convert Orienation from RPY to Quaternion
  tf2::Quaternion orientation;
  orientation.setRPY(-tau/2, 0, 0);

  target_pose_hover.orientation = tf2::toMsg(orientation);
  
  target_pose_hover.position.x = x;
  target_pose_hover.position.y = y;
  target_pose_hover.position.z = z;
  move_group.setPoseTarget(target_pose_hover);

  move_group.move();
  
}

void initPose(moveit::planning_interface::MoveGroupInterface& move_group)
{ 
  moveit::core::RobotStatePtr current_state = move_group.getCurrentState();
  //
  // Next get the current set of joint values for the group.
  std::vector<double> joint_group_positions;
  // Raw pointers are frequently used to refer to the planning group for improved performance.
  const moveit::core::JointModelGroup* joint_model_group =
  move_group.getCurrentState()->getJointModelGroup("panda_arm");
  current_state->copyJointGroupPositions(joint_model_group, joint_group_positions);
  joint_group_positions[0] = 0;
  joint_group_positions[1] = -tau / 8;  // -1/8 turn in radians
  joint_group_positions[2] = 0;
  joint_group_positions[3] = -3 * tau / 8;  // -8/8 turn in radians
  joint_group_positions[4] = 0;
  joint_group_positions[5] = tau / 4 + 0.03;  // 1/4 turn in radians
  joint_group_positions[6] = tau / 8;  // 1/8 turn in radians
  move_group.setJointValueTarget(joint_group_positions);
  //
  // We lower the allowed maximum velocity and acceleration to 5% of their maximum.
  // The default values are 10% (0.1).
  // Set your preferred defaults in the joint_limits.yaml file of your robot's moveit_config
  // or set explicit factors in your code if you need your robot to move faster.
  move_group.setMaxVelocityScalingFactor(0.2); // default 0.05
  move_group.setMaxAccelerationScalingFactor(0.2); // default 0.05
  //
  move_group.move();
}

void pickPose(moveit::planning_interface::MoveGroupInterface& move_group_interface, std::string direction, float x, float y, float z){
  
  moveit::planning_interface::MoveGroupInterface::Plan cartesianPlan;
  move_group_interface.setStartStateToCurrentState();
  move_group_interface.setMaxVelocityScalingFactor(0.01);
  move_group_interface.setMaxAccelerationScalingFactor(0.01);

  std::vector<geometry_msgs::Pose> waypoints;

  geometry_msgs::Pose target_pose_pick = move_group_interface.getCurrentPose().pose;
  target_pose_pick.position.x = x;
  target_pose_pick.position.y = y;
  if (direction == "down"){
    target_pose_pick.position.z = z-0.059;
  }
  else if (direction == "up"){
    target_pose_pick.position.z = z+0.045;
  }
  
  waypoints.push_back(target_pose_pick);

  moveit_msgs::RobotTrajectory trajectory_msg;
  move_group_interface.setPlanningTime(10.0);
  
 
  double fraction = move_group_interface.computeCartesianPath(waypoints,
                                               0.01,  // eef_step
                                               0.0,   // jump_threshold
                                               trajectory_msg, false);
  // Modify trajectory for adjusting speed
  
  // Create robot trajectory object
  robot_trajectory::RobotTrajectory rt(move_group_interface.getCurrentState()->getRobotModel(), "panda_arm");

  // Get robot trajectory
  rt.setRobotTrajectoryMsg(*move_group_interface.getCurrentState(), trajectory_msg);
 
  // Create a IterativeParabolicTimeParameterization object
  trajectory_processing::IterativeParabolicTimeParameterization iptp;

  //Compute TimeStamps
  iptp.computeTimeStamps(rt, 0.1, 0.1);
  
  // Get RobotTrajectory_msg from RobotTrajectory
  rt.getRobotTrajectoryMsg(trajectory_msg);
  cartesianPlan.trajectory_ = trajectory_msg;
  move_group_interface.execute(cartesianPlan);  

}


// Function to transform a point from local to world coordinates
std::tuple<double, double, double> transform_from_local_to_world(double local_x, double local_y, double local_z,
                                                                 double world_x, double world_y, double world_z,
                                                                 double world_roll, double world_pitch, double world_yaw) {
    tf2::Transform transform_world_to_local;
    transform_world_to_local.setOrigin(tf2::Vector3(world_x, world_y, world_z));
    tf2::Quaternion q;
    q.setRPY(world_roll, world_pitch, world_yaw);
    transform_world_to_local.setRotation(q);

    tf2::Vector3 point_local(local_x, local_y, local_z);
    tf2::Vector3 point_world = transform_world_to_local * point_local;

    return std::make_tuple(point_world.getX(), point_world.getY(), point_world.getZ());
}


int main(int argc, char** argv) {
    ros::init(argc, argv, "welding_line_cpp");
    ros::NodeHandle nh;
    //Get information about robot state
    ros::AsyncSpinner spinner(1);
    spinner.start();
    ros::Publisher pose_state_pub = nh.advertise<std_msgs::Int32>("pose_state", 1000); 
    ros::WallDuration(1.0).sleep();
    
    // use for planning scene
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
    // Create MoveGroupInterface for controlling the robot arm
    moveit::planning_interface::MoveGroupInterface move_group("panda_arm");
    move_group.setPlannerId("RRTConnect");
    move_group.setMaxVelocityScalingFactor(0.2);
    move_group.setMaxAccelerationScalingFactor(0.2);
    move_group.setPlanningTime(5.0);

    // Get the position and orientation of the welding line in Gazebo
    ros::ServiceClient get_model_state_client = nh.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");
    gazebo_msgs::GetModelState model_state_srv;
    model_state_srv.request.model_name = "welding_line";

    if (get_model_state_client.call(model_state_srv)) {
        double line_x = model_state_srv.response.pose.position.x;
        double line_y = model_state_srv.response.pose.position.y;
        double line_z = model_state_srv.response.pose.position.z;
        double line_roll, line_pitch, line_yaw;
        tf2::Quaternion quat;
        tf2::fromMsg(model_state_srv.response.pose.orientation, quat);
        tf2::Matrix3x3(quat).getRPY(line_roll, line_pitch, line_yaw);

        // Get dimensions of the welding line model
        double line_length, line_width, line_height; // Assuming these are known or retrieved from model file
        // Assuming the dimensions are retrieved from the model file
        line_length = 1.0; // Placeholder value, replace with actual length
        line_width = 0.2;  // Placeholder value, replace with actual width
        line_height = 0.05; // Placeholder value, replace with actual height

        // Calculate start and end points of the welding line
        double start_local_x = -line_length / 2;
        double start_local_y = 0.0;
        double start_local_z = 0.0;
        double end_local_x = line_length / 2;
        double end_local_y = 0.0;
        double end_local_z = 0.0;

        double start_x, start_y, start_z;
        double end_x, end_y, end_z;

        std::tie(start_x, start_y, start_z) = transform_from_local_to_world(start_local_x, start_local_y, start_local_z,
                                                                            line_x, line_y, line_z,
                                                                            line_roll, line_pitch, line_yaw);
        std::tie(end_x, end_y, end_z) = transform_from_local_to_world(end_local_x, end_local_y, end_local_z,
                                                                      line_x, line_y, line_z,
                                                                      line_roll, line_pitch, line_yaw);

        ROS_INFO("Start position (x, y, z): (%f, %f, %f)", start_x, start_y, start_z);
        ROS_INFO("End position (x, y, z): (%f, %f, %f)", end_x, end_y, end_z);

        // Perform welding operation
        // Assuming the hoverPose and initPose functions are defined
        // Assuming the pickPose function is defined with proper modifications for the welding task
        std_msgs::Int32 state;
        state.data = 1;
        pose_state_pub.publish(state);
        hoverPose(move_group, start_x, start_y, start_z + 0.13);
        
        state.data = 2;
        pose_state_pub.publish(state);
        hoverPose(move_group, end_x, end_y, end_z + 0.13);
        ros::Duration(2.0).sleep(); // Delay for 2 seconds
        // Assuming the initPose function resets the robot to a neutral pose
        state.data = 3;
        pose_state_pub.publish(state);
        initPose(move_group);
        state.data = 4;
        pose_state_pub.publish(state);
        ros::Duration(3.0).sleep(); // Delay for 3 seconds
        ROS_WARN("Round end");
    } else {
        ROS_ERROR("Failed to get model state of welding line");
    }

    ros::shutdown();
    return 0;
}

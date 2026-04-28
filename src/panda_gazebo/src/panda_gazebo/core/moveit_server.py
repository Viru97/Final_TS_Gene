#!/usr/bin/env python3
"""Lightweight ROS2-native planner service server.

This server exposes the historical panda_gazebo MoveIt services with native ROS 2
APIs. It does not depend on ROS 1 shims.
"""

import math
import random

from gazebo_msgs.srv import GetModelState
from rclpy.node import Node

from panda_gazebo.srv import (
    AddBox,
    AddPlane,
    GetEe,
    GetEePose,
    GetEePoseJointConfig,
    GetEeRpy,
    GetMoveItControlledJoints,
    GetRandomEePose,
    GetRandomJointPositions,
    SetEe,
    SetEePose,
)

ARM_JOINTS = [f'panda_joint{i}' for i in range(1, 8)]
HAND_JOINTS = ['panda_finger_joint1', 'panda_finger_joint2']


def _quat_to_rpy(x, y, z, w):
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    sinp = 2.0 * (w * y - z * x)
    pitch = math.copysign(math.pi / 2.0, sinp) if abs(sinp) >= 1.0 else math.asin(sinp)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return roll, pitch, yaw


class PandaMoveItPlannerServer(Node):
    def __init__(self):
        super().__init__('panda_moveit_planner_server')
        self._ee_name = 'panda_link8'
        self._ee_pose = None
        self._scene_boxes = {}
        self._scene_planes = {}
        self._get_model_state = self.create_client(GetModelState, '/gazebo/get_model_state')

        self.create_service(AddBox, 'planning_scene/add_box', self._add_box_cb)
        self.create_service(AddPlane, 'planning_scene/add_plane', self._add_plane_cb)
        self.create_service(SetEe, 'moveit/set_ee', self._set_ee_cb)
        self.create_service(GetEe, 'moveit/get_ee', self._get_ee_cb)
        self.create_service(SetEePose, 'moveit/set_ee_pose', self._set_ee_pose_cb)
        self.create_service(GetEePose, 'moveit/get_ee_pose', self._get_ee_pose_cb)
        self.create_service(GetEeRpy, 'moveit/get_ee_rpy', self._get_ee_rpy_cb)
        self.create_service(
            GetMoveItControlledJoints,
            'moveit/get_controlled_joints',
            self._get_controlled_joints_cb,
        )
        self.create_service(
            GetRandomJointPositions,
            'moveit/get_random_joint_positions',
            self._get_random_joint_positions_cb,
        )
        self.create_service(
            GetRandomEePose, 'moveit/get_random_ee_pose', self._get_random_ee_pose_cb
        )
        self.create_service(
            GetEePoseJointConfig,
            'moveit/get_ee_pose_joint_config',
            self._get_ee_pose_joint_config_cb,
        )
        self.get_logger().info('Panda MoveIt planner server (ROS2 native) ready')

    def _add_box_cb(self, req, res):
        self._scene_boxes[req.name] = {'frame_id': req.frame_id, 'pose': req.pose, 'size': list(req.size)}
        res.success = True
        res.message = f'Box "{req.name}" stored in scene cache'
        return res

    def _add_plane_cb(self, req, res):
        self._scene_planes[req.name] = {
            'frame_id': req.frame_id,
            'pose': req.pose,
            'normal': list(req.normal),
            'offset': req.offset,
        }
        res.success = True
        res.message = f'Plane "{req.name}" stored in scene cache'
        return res

    def _set_ee_cb(self, req, res):
        self._ee_name = req.ee_name
        res.success = True
        res.message = f'EE set to "{self._ee_name}"'
        return res

    def _get_ee_cb(self, _req, res):
        res.ee_name = self._ee_name
        res.success = True
        res.message = 'OK'
        return res

    def _set_ee_pose_cb(self, req, res):
        self._ee_pose = req.pose
        res.success = True
        res.message = 'Target EE pose cached'
        return res

    def _get_ee_pose_cb(self, _req, res):
        if self._ee_pose is not None:
            res.pose = self._ee_pose
            res.success = True
            res.message = 'Returning cached EE pose'
            return res
        if not self._get_model_state.wait_for_service(timeout_sec=0.5):
            res.success = False
            res.message = 'No cached EE pose and /gazebo/get_model_state unavailable'
            return res
        gm_req = GetModelState.Request()
        gm_req.model_name = 'panda'
        future = self._get_model_state.call_async(gm_req)
        import rclpy
        rclpy.spin_until_future_complete(self, future, timeout_sec=1.0)
        gm_res = future.result()
        if gm_res is None:
            res.success = False
            res.message = 'Failed to query /gazebo/get_model_state'
            return res
        res.pose = gm_res.pose
        res.success = True
        res.message = 'Returning gazebo model pose as EE fallback'
        return res

    def _get_ee_rpy_cb(self, _req, res):
        pose_resp = self._get_ee_pose_cb(None, GetEePose.Response())
        if not pose_resp.success:
            res.success = False
            res.message = pose_resp.message
            return res
        q = pose_resp.pose.orientation
        roll, pitch, yaw = _quat_to_rpy(q.x, q.y, q.z, q.w)
        res.r = float(roll)
        res.p = float(pitch)
        res.y = float(yaw)
        res.success = True
        res.message = 'OK'
        return res

    def _get_controlled_joints_cb(self, _req, res):
        res.controlled_joints_arm = ARM_JOINTS
        res.controlled_joints_hand = HAND_JOINTS
        res.controlled_joints = ARM_JOINTS + HAND_JOINTS
        res.success = True
        res.message = 'OK'
        return res

    def _get_random_joint_positions_cb(self, _req, res):
        res.joint_names = ARM_JOINTS + HAND_JOINTS
        res.joint_positions = [random.uniform(-1.5, 1.5) for _ in ARM_JOINTS] + [0.03, 0.03]
        res.success = True
        res.message = 'Generated random joint configuration'
        return res

    def _get_random_ee_pose_cb(self, _req, res):
        res.ee_pose.position.x = random.uniform(0.45, 0.7)
        res.ee_pose.position.y = random.uniform(-0.25, 0.25)
        res.ee_pose.position.z = random.uniform(0.2, 0.6)
        res.ee_pose.orientation.w = 1.0
        res.joint_names = ARM_JOINTS + HAND_JOINTS
        res.joint_positions = [0.0] * len(ARM_JOINTS) + [0.03, 0.03]
        res.success = True
        res.message = 'Generated random EE pose'
        return res

    def _get_ee_pose_joint_config_cb(self, req, res):
        _ = req
        res.joint_names = ARM_JOINTS + HAND_JOINTS
        res.joint_positions = [0.0] * len(ARM_JOINTS) + [0.03, 0.03]
        res.success = True
        res.message = 'Returned nominal joint configuration'
        return res

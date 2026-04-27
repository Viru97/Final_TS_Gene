#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32, Int32


class FaultInjector(Node):
    def __init__(self):
        super().__init__('fault_injector')

        self.joint_index = None
        self.fault_amplitude = None
        self.fault_duration = None
        self.start_time = None
        self._fault_is_active = False

        self.faulty_joint_pub = self.create_publisher(JointState, 'faulty_joint_states', 100)
        self.fault_flag_pub = self.create_publisher(Int32, 'fault_flag', 100)

        self.create_subscription(Float32, '/fault_time', self._on_fault_time, 50)
        self.create_subscription(Int32, '/fault_index', self._on_fault_index, 50)
        self.create_subscription(Float32, '/fault_amplitude', self._on_fault_amplitude, 50)
        self.create_subscription(Float32, '/fault_duration', self._on_fault_duration, 50)
        self.create_subscription(JointState, '/joint_states', self._on_joint_state, 100)

    def _on_fault_time(self, msg: Float32):
        self.start_time = float(msg.data)

    def _on_fault_index(self, msg: Int32):
        self.joint_index = int(msg.data)

    def _on_fault_amplitude(self, msg: Float32):
        self.fault_amplitude = float(msg.data)

    def _on_fault_duration(self, msg: Float32):
        self.fault_duration = float(msg.data)

    def _all_fault_inputs_ready(self):
        return (
            self.joint_index is not None
            and self.fault_amplitude is not None
            and self.fault_duration is not None
            and self.start_time is not None
        )

    def _fault_should_be_active(self, now_sec: float):
        if not self._all_fault_inputs_ready():
            return False
        elapsed = now_sec - self.start_time
        return elapsed >= 0.0 and elapsed < self.fault_duration

    def _publish_fault_flag(self, active: bool):
        flag = Int32()
        flag.data = 1 if active else 0
        self.fault_flag_pub.publish(flag)

    def _copy_joint_state(self, msg: JointState):
        out = JointState()
        out.header = msg.header
        out.name = list(msg.name)
        out.position = list(msg.position)
        out.velocity = list(msg.velocity)
        out.effort = list(msg.effort)
        return out

    def _on_joint_state(self, msg: JointState):
        joint_msg = self._copy_joint_state(msg)
        now_sec = self.get_clock().now().nanoseconds / 1e9
        fault_active = self._fault_should_be_active(now_sec)

        if fault_active and 0 <= self.joint_index < len(joint_msg.position):
            joint_msg.position[self.joint_index] += self.fault_amplitude

        if fault_active != self._fault_is_active:
            self._fault_is_active = fault_active
            if fault_active:
                self.get_logger().warning('Fault injection started')
            else:
                self.get_logger().warning('Fault injection ended')

        self._publish_fault_flag(fault_active)
        self.faulty_joint_pub.publish(joint_msg)


def main(args=None):
    rclpy.init(args=args)
    node = FaultInjector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

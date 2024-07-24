#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64, Float64MultiArray
from sensor_msgs.msg import JointState
from open_manipulator_controller import OpenManipulatorController
from gripper_controller import GripperController
from motion_sequence_controller import MotionSequenceController

if __name__ == '__main__':
    rospy.init_node("open_manipulator_controller", anonymous=True)
    manipulator_controller = OpenManipulatorController()
    gripper_controller = GripperController("/gripper_position/command")
    motion_sequence_controller = MotionSequenceController(manipulator_controller, gripper_controller)
    
    positions_sequence = [
        (0.286, 0.00, 0.05),
        (0.286, 0.00, 0.205),
        (0.000, 0.28, 0.05)
    ]
    
    motion_sequence_controller.move_through_sequence(positions_sequence)
    
    jnames = ['joint1', 'joint2', 'joint3', 'joint4']
    jstate = JointState()
    jstate.name = jnames

    rate = rospy.Rate(10)
    while not rospy.is_shutdown() and not motion_sequence_controller.sequence_completed:
        jstate.header.stamp = rospy.Time.now()
        jstate.position = manipulator_controller.move_to_position(*positions_sequence[-1])[0]
        manipulator_controller.joint_state_pub.publish(jstate)
        rate.sleep()

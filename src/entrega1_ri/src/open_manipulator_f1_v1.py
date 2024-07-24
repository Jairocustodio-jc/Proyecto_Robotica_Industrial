#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from markers import BallMarker, color
from functions import fkine_open_manipulator

class OpenManipulatorController:
    def __init__(self):
        # Define joint limits
        self.joint_limits = {
            'joint1': (-3.142, 3.142),
            'joint2': (-1.5708, 1.5708),
            'joint3': (-1.5708, 1.5708),
            'joint4': (-1.5708, 1.5708)
        }

        # Define joint topics
        self.joint_topics = {
            'joint1': "/joint1_position/command",
            'joint2': "/joint2_position/command",
            'joint3': "/joint3_position/command",
            'joint4': "/joint4_position/command"
        }

    def send_joint_position(self, joint_name, position):
        # Check if the position is within the limits
        if not (self.joint_limits[joint_name][0] <= position <= self.joint_limits[joint_name][1]):
            rospy.logerr("Position %f out of limits for %s", position, joint_name)
            return
        
        pub = rospy.Publisher(self.joint_topics[joint_name], Float64, queue_size=10)
        rospy.sleep(1)  # Wait a moment to ensure the connection is established
        msg = Float64()
        msg.data = position
        pub.publish(msg)
        rospy.loginfo("Position sent to %s: %f", joint_name, position)

    def send_joint_positions(self, positions):
        # Send positions to each joint
        for joint_name, position in positions.items():
            self.send_joint_position(joint_name, position)


if __name__ == '__main__':
    rospy.init_node("testForwardKinematics", anonymous=True)
    bmarker = BallMarker(color['GREEN'])
    controller = OpenManipulatorController()
    
    # Joint configuration
    q = {'joint1': 0, 'joint2': 0.3, 'joint3': 0.3, 'joint4': 0}
    
    # Send the joint positions to the robot
    controller.send_joint_positions(q)
    
    # Create a rate object
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        # Calculate the end effector position with respect to the base
        T = fkine_open_manipulator(list(q.values()))
        
        # Update the marker position and publish
        bmarker.position(T)
        bmarker.publish()
        
        # Sleep to maintain the loop rate
        rate.sleep()

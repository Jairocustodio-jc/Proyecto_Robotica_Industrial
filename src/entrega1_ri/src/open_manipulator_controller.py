import rospy
import numpy as np
from std_msgs.msg import Float64, Float64MultiArray
from sensor_msgs.msg import JointState
from functions import ik_gradient_open_manipulator, fkine_open_manipulator

class OpenManipulatorController:
    def __init__(self):
        self.joint_limits = {
            'joint1': (-3.142, 3.142),
            'joint2': (-1.5708, 1.5708),
            'joint3': (-1.5708, 1.5708),
            'joint4': (-1.5708, 1.5708)
        }
        self.joint_topics = {
            'joint1': "/joint1_position/command",
            'joint2': "/joint2_position/command",
            'joint3': "/joint3_position/command",
            'joint4': "/joint4_position/command"
        }
        self.ee_pos_pub = rospy.Publisher('end_effector_position', Float64MultiArray, queue_size=10)
        self.joint_state_pub = rospy.Publisher('joint_states', JointState, queue_size=10)

    def send_joint_position(self, joint_name, position):
        if not (self.joint_limits[joint_name][0] <= position <= self.joint_limits[joint_name][1]):
            rospy.logerr("Position %f out of limits for %s", position, joint_name)
            return
        
        pub = rospy.Publisher(self.joint_topics[joint_name], Float64, queue_size=10)
        rospy.sleep(0.2)
        msg = Float64()
        msg.data = position
        pub.publish(msg)
        rospy.loginfo("Position sent to %s: %f", joint_name, position)

    def send_joint_positions(self, positions):
        for joint_name, position in positions.items():
            self.send_joint_position(joint_name, position)

    def move_to_position(self, x, y, z):
        q0 = [0, 0, 0, 0]
        xdes = np.array([x, y, z])
        q_sol = ik_gradient_open_manipulator(xdes, q0)
        q_dict = {
            'joint1': q_sol[0],
            'joint2': q_sol[1],
            'joint3': q_sol[2],
            'joint4': q_sol[3]
        }
        self.send_joint_positions(q_dict)
        T = fkine_open_manipulator(q_sol)
        ee_position = T[0:3, 3]
        ee_msg = Float64MultiArray(data=ee_position)
        self.ee_pos_pub.publish(ee_msg)
        return q_sol, ee_position

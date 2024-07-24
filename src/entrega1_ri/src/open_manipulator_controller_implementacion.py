import rospy
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from sensor_msgs.msg import JointState
import numpy as np
from functions import ik_gradient_open_manipulator

class OpenManipulatorController:
    def __init__(self):
        rospy.wait_for_service('/goal_joint_space_path')
        self.set_joint_position = rospy.ServiceProxy('/goal_joint_space_path', SetJointPosition)
        rospy.Subscriber('/open_manipulator/joint_states', JointState, self.joint_state_callback)
        self.joint_states = None

    def joint_state_callback(self, msg):
        self.joint_states = msg

    def move_to_joint_positions(self, positions):
        req = SetJointPositionRequest()
        req.joint_position.joint_name = ["joint1", "joint2", "joint3", "joint4"]
        req.joint_position.position = positions
        req.path_time = 2.0
        try:
            resp = self.set_joint_position(req)
            return resp
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")

    def get_current_joint_states(self):
        return self.joint_states.position if self.joint_states else None

    def move_to_position(self, x, y, z, fixed_joint_index=None, fixed_joint_value=None):
        xdes = np.array([x, y, z])
        if self.joint_states:
            q0 = np.array(self.joint_states.position)
        else:
            q0 = np.zeros(4)

        q_des = ik_gradient_open_manipulator(xdes, q0, fixed_joint_index, fixed_joint_value)

        rospy.loginfo(f"Posición deseada: {xdes}")
        rospy.loginfo(f"Ángulos calculados de las articulaciones: {q_des}")

        result = self.move_to_joint_positions(q_des)
        if result:
            rospy.loginfo("Move to position successful.")
        else:
            rospy.logwarn("Move to position failed.")

if __name__ == '__main__':
    controller = OpenManipulatorController()
    
    # Ejemplo sin especificar una articulación fija
    controller.move_to_position(0.1, 0.2, 0.3)
    
    # Ejemplo especificando una articulación fija
    controller.move_to_position(0.1, 0.2, 0.3, fixed_joint_index=0, fixed_joint_value=np.pi/4)
    
    rospy.spin()

#!/usr/bin/env python3
import rospy
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest

class GripperController:
    def __init__(self):
        # Esperar a que el servicio del gripper esté disponible
        rospy.wait_for_service('/goal_tool_control')
        self.set_gripper_position = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)

    def set_gripper(self, position):
        """
        Establecer la posición del gripper.
        
        Args:
        - position: Posición deseada del gripper (normalmente 0.01 para abrir y -0.01 para cerrar)
        """
        req = SetJointPositionRequest()
        req.joint_position.joint_name = ["gripper"]
        req.joint_position.position = [position]
        req.path_time = 1.0  # Tiempo para mover el gripper
        try:
            resp = self.set_gripper_position(req)
            return resp
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
            return None

    def open_gripper(self):
        rospy.loginfo("Abriendo el gripper")
        return self.set_gripper(0.01)  # Ajusta el valor según sea necesario

    def close_gripper(self):
        rospy.loginfo("Cerrando el gripper")
        return self.set_gripper(-0.01)  # Ajusta el valor según sea necesario

    def move_gripper_to_position(self, position):
        """
        Mueve el gripper a una posición específica.

        Args:
        - position: Posición deseada del gripper.
        """
        rospy.loginfo(f"Moviendo el gripper a la posición: {position}")
        return self.set_gripper(position)


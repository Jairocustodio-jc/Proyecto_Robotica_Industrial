#!/usr/bin/env python3
import rospy
from motion_sequence_controller_implementacion import MotionSequenceController
from gripper_controller_implementacion import GripperController

class ObjectManipulationController:
    def __init__(self):
        self.motion_controller = MotionSequenceController()
        self.gripper_controller = GripperController()

    def execute_pick_and_place(self, positions):
        """
        Ejecuta la secuencia de recoger y colocar un objeto.

        Args:
        - positions: Lista de tuplas, donde cada tupla es una posición (x, y, z).
        """
        rospy.loginfo("Iniciando secuencia de recogida y colocación")

         # Ir a la posición 0
        rospy.loginfo("Moviendo a la posición 0")
        self.motion_controller.controller.move_to_position(*positions[4])
        rospy.sleep(2)  # Esperar a que el robot llegue a la posición

        # # Ir a la posición 1
        # rospy.loginfo("Moviendo a la posición 1")
        # self.motion_controller.controller.move_to_position(*positions[0])
        # rospy.sleep(2)  # Esperar a que el robot llegue a la posición

        # # Cerrar el gripper para recoger el objeto
        # rospy.loginfo("Cerrando el gripper para recoger el objeto")
        # self.gripper_controller.move_gripper_to_position(0)
        # rospy.sleep(2)  # Esperar a que el gripper se cierre
        
        # # Ir a la posición 2
        # rospy.loginfo("Moviendo a la posición 2")
        # self.motion_controller.controller.move_to_position(*positions[1])
        # rospy.sleep(0.5)  # Esperar a que el robot llegue a la posición

        # # Ir a la posición 3
        # rospy.loginfo("Moviendo a la posición 3")
        # self.motion_controller.controller.move_to_position(*positions[2])
        # rospy.sleep(2)  # Esperar a que el robot llegue a la posición

        # # Abrir el gripper para dejar el objeto
        # rospy.loginfo("Abriendo el gripper para dejar el objeto")
        # self.gripper_controller.open_gripper()
        # rospy.sleep(2)  # Esperar a que el gripper se abra
        
        # # Ir a la posición 4
        # rospy.loginfo("Moviendo a la posición 4")
        # self.motion_controller.controller.move_to_position(*positions[3])
        # rospy.sleep(2)  # Esperar a que el robot llegue a la posición

if __name__ == '__main__':
    rospy.init_node('object_manipulation_controller', anonymous=True)
    object_manipulation_controller = ObjectManipulationController()

    # Definir una secuencia de posiciones
    positions_sequence = [       
        (0.25, 0.00, 0.05),
        (0.286, 0.00, 0.205),
        (0.000, 0.28, 0.05),
        (0.286, 0.00, 0.205),
        (0.229,-0.006,0.025),
    ]

    # Ejecutar la secuencia de recoger y colocar
    object_manipulation_controller.execute_pick_and_place(positions_sequence)

    # Mantener el nodo en ejecución
    rospy.spin()

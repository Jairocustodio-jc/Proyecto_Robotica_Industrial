#!/usr/bin/env python3
import rospy
from open_manipulator_controller_implementacion import OpenManipulatorController

class MotionSequenceController:
    def __init__(self):
        self.controller = OpenManipulatorController()

    def move_through_sequence(self, positions):
        """
        Mueve el robot a través de una secuencia de posiciones.
        
        Args:
        - positions: Lista de tuplas, donde cada tupla es una posición (x, y, z).
        """
        for position in positions:
            x, y, z = position
            rospy.loginfo(f"Moviendo a posición: x={x}, y={y}, z={z}")
            self.controller.move_to_position(x, y, z)
            rospy.sleep(2)  # Espera un tiempo antes de moverse a la siguiente posición
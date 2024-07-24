#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

class OpenManipulatorController:
    def __init__(self):
        # Inicializa el nodo ROS
        rospy.init_node('send_joint_positions', anonymous=True)

        # Definir rangos permitidos para las articulaciones
        self.joint_limits = {
            'joint1': (-3.142, 3.142),
            'joint2': (-1.5708, 1.5708),
            'joint3': (-1.5708, 1.5708),
            'joint4': (-1.5708, 1.5708)
        }

        # Nombres de los tópicos de las articulaciones
        self.joint_topics = {
            'joint1': "/joint1_position/command",
            'joint2': "/joint2_position/command",
            'joint3': "/joint3_position/command",
            'joint4': "/joint4_position/command"
        }

    def send_joint_position(self, joint_name, position):
        # Verificar si la posición está dentro de los límites permitidos
        if not (self.joint_limits[joint_name][0] <= position <= self.joint_limits[joint_name][1]):
            rospy.logerr("Posición %f fuera de los límites para %s", position, joint_name)
            return
        
        pub = rospy.Publisher(self.joint_topics[joint_name], Float64, queue_size=10)
        rospy.sleep(1)  # Espera un momento para asegurar que la conexión se establezca
        msg = Float64()
        msg.data = position
        pub.publish(msg)
        rospy.loginfo("Posición enviada a %s: %f", joint_name, position)

    def send_joint_positions(self, positions):
        # Enviar posiciones a cada articulación
        for joint_name, position in positions.items():
            self.send_joint_position(joint_name, position)
        
        # Mantén el nodo corriendo para asegurar que los mensajes se envíen
        rospy.spin()

if __name__ == '__main__':
    try:
        controller = OpenManipulatorController()

        # Posiciones deseadas para las articulaciones (en radianes)
        positions = {
            'joint1': 0.0,
            'joint2': 0.0,
            'joint3': 0.0,
            'joint4': 0.0
        }

        controller.send_joint_positions(positions)
        
    except rospy.ROSInterruptException:
        pass

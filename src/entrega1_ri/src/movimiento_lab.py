#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from time import sleep
from sensor_msgs.msg import LaserScan
from entrega1_ri.msg import ArrayXY
import numpy as np
import tf

# Función para mover el TurtleBot3
def move_turtlebot3(distance, speed, is_forward):
    # Check for zero speed
    if speed == 0:
        return
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    # Instancia de Twist para los comandos de velocidad
    vel_msg = Twist()

    # Establecer la dirección del movimiento
    if is_forward:
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    # Tiempo de movimiento basado en la velocidad y distancia
    travel_time = distance / speed

    # Publicar la velocidad y mover el robot
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < travel_time:
        velocity_publisher.publish(vel_msg)
        sleep(0.1)

    # Detener el robot
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

# Función para girar el TurtleBot3
def rotate_turtlebot3(angle, speed, clockwise):
    # Publicador para el tópico 'cmd_vel'
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    # Instancia de Twist para los comandos de velocidad
    vel_msg = Twist()

    # Establecer la velocidad angular
    vel_msg.angular.z = abs(speed) if clockwise else -abs(speed)

    # Tiempo de rotación basado en la velocidad y ángulo
    rotation_time = angle / speed

    # Publicar la velocidad y girar el robot
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < rotation_time:
        velocity_publisher.publish(vel_msg)
        sleep(0.1)

    # Detener el robot
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

# Callback para el LiDAR
def lidar_callback(msg):
    # Comprobar si hay algún objeto demasiado cerca
    ranges = np.sqrt(np.array(msg.x)**2 + np.array(msg.y)**2)
    if np.min(ranges) < 0.35:  # Adjust threshold as needed
        rospy.loginfo("Objeto muy cerca deteniendo robot")
        move_turtlebot3(0, 0, True)  # Stop the robot

if __name__ == '__main__':
    try:
        # Inicializar el nodo de ROS
        rospy.init_node('turtlebot3_controller', anonymous=True)
        # Suscribirse al tópico del LiDAR para detectar objetos cercanos
        rospy.Subscriber('lidar_xy', ArrayXY, lidar_callback)

        # Broadcast the initial transform
        tf_broadcaster = tf.TransformBroadcaster()
        tf_broadcaster.sendTransform((0, 0, 0), tf.transformations.quaternion_from_euler(0, 0, 0),
                                     rospy.Time.now(), "base_link", "map")

        # Mover 3 metros hacia adelante
        move_turtlebot3(3, 0.2, True)
        # Girar 90 grados hacia la izquierda
        rotate_turtlebot3(1.57, 0.2, False)
        # Mover 2 metros hacia adelante
        move_turtlebot3(2, 0.2, True)

    except rospy.ROSInterruptException:
        pass

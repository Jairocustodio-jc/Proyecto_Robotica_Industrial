#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from entrega1_ri.msg import ArrayXY
import numpy as np

# Variables globales
object_detected_time = None
object_is_near = False
object_is_near_2s = False
current_pose = Pose()
initial_pose = Pose()  # Nueva variable para almacenar la posición inicial
y_movement_completed = False  # Bandera para indicar si el movimiento en Y ha terminado
x_movement_completed = False  # Bandera para indicar si el movimiento en X ha terminado
rotation_completed = False     # Bandera para indicar si la rotación ha terminado

# Callback para el odómetro
def odom_callback(msg):
    global current_pose
    current_pose = msg.pose.pose

# Función para mover el TurtleBot3 una distancia específica en el eje x usando el odómetro
def move_turtlebot3(distance, speed, is_forward, velocity_publisher, object_is_near, initial_pose, current_pose):
    vel_msg = Twist()
    start_x = initial_pose.position.x
    start_y = initial_pose.position.y
    if is_forward:
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    distance_moved_x = np.abs(current_pose.position.x - start_x)
    distance_moved_y = np.abs(current_pose.position.y - start_y)
    distance_moved = np.sqrt(distance_moved_x**2 + distance_moved_y**2)
    
    if object_is_near or distance_moved >= distance:
        vel_msg.linear.x = 0
        velocity_publisher.publish(vel_msg)
        if distance_moved >= distance:
            print("Movimiento culminado en X_Y")
            return True
    else:
        velocity_publisher.publish(vel_msg)
    return False

def rotate_turtlebot3(angle, angular_speed, is_clockwise, velocity_publisher, object_is_near, initial_pose, current_pose):
    vel_msg = Twist()
    if is_clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    # Convertimos el ángulo a radianes
    angle_radians = np.deg2rad(angle)
    start_yaw = initial_pose.orientation.z

    current_yaw = 2 * np.arctan2(current_pose.orientation.z, current_pose.orientation.w)
    angle_moved = np.abs(current_yaw - start_yaw)

    if object_is_near or angle_moved >= angle_radians:
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        if angle_moved >= angle_radians:
            print("Rotación completada")
            return True
    else:
        velocity_publisher.publish(vel_msg)
    return False

# Callback para el LiDAR
def lidar_callback(msg):
    global object_detected_time, object_is_near, object_is_near_2s
    ranges = np.sqrt(np.array(msg.x)**2 + np.array(msg.y)**2)
    min_distance = np.min(ranges)

    if min_distance < 0.45:
        if object_detected_time is None:
            object_detected_time = rospy.Time.now().to_sec()
            object_is_near = True
        else:
            elapsed_time = rospy.Time.now().to_sec() - object_detected_time
            print(f"Segundos pasados desde la detección del objeto: {elapsed_time}")
            if elapsed_time > 2:
                object_is_near_2s = True
                object_is_near = True
                rospy.loginfo("Objeto cerca demasiado tiempo")
    else:
        if not object_is_near_2s:
            object_detected_time = None
            object_is_near = False
            object_is_near_2s = False

if __name__ == '__main__':
    rospy.init_node('turtlebot3_controller', anonymous=True)
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.Subscriber('lidar_xy', ArrayXY, lidar_callback)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.sleep(1)
    # Reiniciar el sistema de referencia
    initial_pose = Pose()
    rate = rospy.Rate(100)    # 10hz
    while not rospy.is_shutdown():
        # Moverse 2 metro en x
        x_movement_completed = move_turtlebot3(
            distance=2.0, 
            speed=0.2, 
            is_forward=True, 
            velocity_publisher=velocity_publisher, 
            object_is_near=object_is_near, 
            initial_pose=initial_pose, 
            current_pose=current_pose
        )
        
        if x_movement_completed and not rotation_completed:
            # Rotar 90 grados después de completar el movimiento en X
            rotation_completed = rotate_turtlebot3(
                angle=90, 
                angular_speed=0.1, 
                is_clockwise=True, 
                velocity_publisher=velocity_publisher, 
                object_is_near=object_is_near, 
                initial_pose=initial_pose, 
                current_pose=current_pose
            )
        
        if x_movement_completed and rotation_completed:
            # Moverse 2 metros en la dirección y
            y_movement_completed = move_turtlebot3(
                distance=2.83, 
                speed=0.2, 
                is_forward=True, 
                velocity_publisher=velocity_publisher, 
                object_is_near=object_is_near, 
                initial_pose=initial_pose, 
                current_pose=current_pose
            )
        rate.sleep()

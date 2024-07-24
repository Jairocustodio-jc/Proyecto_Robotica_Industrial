#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, PointStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt, radians
import time

class PositionController:
    def __init__(self, targets, pos_kp, pos_ki, pos_kd, orient_kp, orient_ki, orient_kd, tolerance=0.01):
        rospy.init_node('position_controller')
        rospy.Subscriber('/odom', Odometry, self.odometry_callback)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pos_pub = rospy.Publisher('/robot_position', PointStamped, queue_size=10)
        self.orient_pub = rospy.Publisher('/robot_orientation', PointStamped, queue_size=10)
        self.targets = targets  # Lista de objetivos [(x, y, yaw_degrees), ...]
        self.target_index = 0
        self.tolerance = tolerance
        self.rate = rospy.Rate(10)
        self.pos_kp = pos_kp
        self.pos_ki = pos_ki
        self.pos_kd = pos_kd
        self.orient_kp = orient_kp
        self.orient_ki = orient_ki
        self.orient_kd = orient_kd
        self.prev_pos_error = 0.0
        self.pos_error_sum = 0.0
        self.prev_orient_error = 0.0
        self.orient_error_sum = 0.0
        self.cmd_vel = Twist()
        self.start_time = time.time()
        self.position_reached = False

    def odometry_callback(self, odom):
        x = odom.pose.pose.position.x
        y = odom.pose.pose.position.y
        orientation_q = odom.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        current_time = time.time() - self.start_time

        # Publicar datos de posición
        pos_msg = PointStamped()
        pos_msg.header.stamp = rospy.Time.now()
        pos_msg.point.x = x
        pos_msg.point.y = y
        pos_msg.point.z = current_time
        self.pos_pub.publish(pos_msg)

        # Publicar datos de orientación
        orient_msg = PointStamped()
        orient_msg.header.stamp = rospy.Time.now()
        orient_msg.point.x = yaw
        orient_msg.point.y = 0
        orient_msg.point.z = current_time
        self.orient_pub.publish(orient_msg)

        if not self.position_reached:
            distance_error = sqrt((self.targets[self.target_index][0] - x)**2 + (self.targets[self.target_index][1] - y)**2)
            angle_error = atan2(self.targets[self.target_index][1] - y, self.targets[self.target_index][0] - x) - yaw

            # Ensure angle is within -pi to pi
            if angle_error > 3.14159:
                angle_error -= 2 * 3.14159
            elif angle_error < -3.14159:
                angle_error += 2 * 3.14159

            # PID control for position
            self.pos_error_sum += angle_error
            angle_speed = self.pos_kp * angle_error + self.pos_ki * self.pos_error_sum + self.pos_kd * (angle_error - self.prev_pos_error)
            self.prev_pos_error = angle_error

            # Command velocity
            self.cmd_vel.angular.z = angle_speed
            self.cmd_vel.linear.x = distance_error * self.pos_kp

            # Publish velocity command
            self.cmd_pub.publish(self.cmd_vel)

            # Check if target reached
            if distance_error < self.tolerance:
                rospy.loginfo(f"Target {self.target_index+1} position reached!")
                self.cmd_vel.angular.z = 0.0
                self.cmd_vel.linear.x = 0.0
                self.cmd_pub.publish(self.cmd_vel)
                self.position_reached = True
                self.pos_error_sum = 0.0  # Reset integral term for the next phase
                self.prev_pos_error = 0.0  # Reset previous error for the next phase
        else:
            # Adjust orientation to match the final yaw
            final_yaw = radians(self.targets[self.target_index][2])
            angle_error = final_yaw - yaw

            # Ensure angle is within -pi to pi
            if angle_error > 3.14159:
                angle_error -= 2 * 3.14159
            elif angle_error < -3.14159:
                angle_error += 2 * 3.14159

            # PID control for orientation
            self.orient_error_sum += angle_error
            angle_speed = self.orient_kp * angle_error + self.orient_ki * self.orient_error_sum + self.orient_kd * (angle_error - self.prev_orient_error)
            self.prev_orient_error = angle_error

            # Command velocity
            self.cmd_vel.angular.z = angle_speed
            self.cmd_vel.linear.x = 0.0

            # Publish velocity command
            self.cmd_pub.publish(self.cmd_vel)

            if abs(angle_error) < 0.01:  # If the angle error is small enough, stop
                rospy.loginfo(f"Target {self.target_index+1} orientation adjusted!")
                self.cmd_vel.angular.z = 0.0
                self.cmd_pub.publish(self.cmd_vel)
                self.position_reached = False
                self.orient_error_sum = 0.0  # Reset integral term for the next phase
                self.prev_orient_error = 0.0  # Reset previous error for the next phase
                self.target_index += 1
                if self.target_index >= len(self.targets):
                    rospy.loginfo("All targets reached!")
                    rospy.signal_shutdown("All targets reached")

    def run(self):
        rospy.loginfo("Position controller running...")
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    try:
        pos_kp = 0.08  # Proporcional para posición
        pos_ki = 0.001  # Integral para posición
        pos_kd = 0.02  # Derivativo para posición
        orient_kp = 0.01  # Proporcional para orientación
        orient_ki = 0.001 # Integral para orientación
        orient_kd = 0.005 # Derivativo para orientación
        targets = [
            (1.0, 0.0, -90),  # Primer objetivo (x, y, yaw en grados)
            (1.0, -1.0, -90.0)   # Segundo objetivo (x, y, yaw en grados)
        ]
        controller = PositionController(targets=targets, 
                                        pos_kp=pos_kp, pos_ki=pos_ki, pos_kd=pos_kd, 
                                        orient_kp=orient_kp, orient_ki=orient_ki, orient_kd=orient_kd)
        controller.run()
    except rospy.ROSInterruptException:
        pass

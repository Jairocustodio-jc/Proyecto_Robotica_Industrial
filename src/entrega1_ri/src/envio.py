#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def rotate_robot():
    rospy.init_node('rotate_robot', anonymous=True)
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    twist = Twist()
    rotate_speed = 0.5  # rad/s
    rotate_duration = 1.57 / rotate_speed  # 90 degrees (pi/2 rad)

    # Rotate 90 degrees to the right
    twist.angular.z = -rotate_speed
    cmd_vel_pub.publish(twist)
    rospy.sleep(rotate_duration)

    # Stop
    twist.angular.z = 0
    cmd_vel_pub.publish(twist)
    rospy.sleep(1)

    # Rotate 90 degrees to the left to return to the initial orientation
    twist.angular.z = rotate_speed
    cmd_vel_pub.publish(twist)
    rospy.sleep(rotate_duration)

    # Stop
    twist.angular.z = 0
    cmd_vel_pub.publish(twist)

    # Closing the program
    rospy.signal_shutdown('Completed rotation sequence')

if __name__ == '__main__':
    try:
        rotate_robot()
    except rospy.ROSInterruptException:
        pass

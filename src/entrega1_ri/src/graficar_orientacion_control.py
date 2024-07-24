#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimeOrientationPlotter:
    def __init__(self):
        rospy.init_node('real_time_orientation_plotter')
        rospy.Subscriber('/robot_orientation', PointStamped, self.orientation_callback)
        self.orientations = []
        self.times = []
        self.fig, self.ax = plt.subplots()
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100)
        plt.show()

    def orientation_callback(self, msg):
        self.orientations.append(msg.point.x)
        self.times.append(msg.point.z)

    def update_plot(self, frame):
        self.ax.clear()
        self.ax.plot(self.times, self.orientations, label='Yaw')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Orientation (radians)')
        self.ax.legend()
        self.ax.set_title('Orientation (Yaw) vs Time')

if __name__ == '__main__':
    try:
        RealTimeOrientationPlotter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

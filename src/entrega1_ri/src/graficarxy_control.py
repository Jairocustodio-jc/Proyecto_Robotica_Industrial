#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimePlotter:
    def __init__(self):
        rospy.init_node('real_time_plotter')
        rospy.Subscriber('/robot_position', PointStamped, self.position_callback)
        self.positions_x = []
        self.positions_y = []
        self.times = []
        self.fig, self.ax = plt.subplots()
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100)
        plt.show()

    def position_callback(self, msg):
        self.positions_x.append(msg.point.x)
        self.positions_y.append(msg.point.y)
        self.times.append(msg.point.z)

    def update_plot(self, frame):
        self.ax.clear()
        self.ax.plot(self.times, self.positions_x, label='Position X')
        self.ax.plot(self.times, self.positions_y, label='Position Y')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Position')
        self.ax.legend()
        self.ax.set_title('Position (X, Y) vs Time')

if __name__ == '__main__':
    try:
        RealTimePlotter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore",".*GUI is implemented.*")

import rospy
from entrega1_ri.msg import ArrayXY
import matplotlib.animation as animation

# Initialize empty arrays to store data
x_data = []
y_data = []

def plot_xy(msg):
    """
    Callback function to plot x and y data points.
    
    Args:
    msg (ArrayXY): Message containing x and y arrays.
    """
    global x_data, y_data
    x_data = msg.x
    y_data = msg.y

def update_plot(frame):
    """
    Update function for the animation.
    
    Args:
    frame (int): Frame number (not used).
    
    Returns:
    tuple: Updated plot objects.
    """
    global x_data, y_data
    plt.cla()
    plt.plot(x_data, y_data, 'b.')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    ax = plt.gca()
    ax.axis("equal")
    ax.set_xlim([-5, 5])  # Set x-axis limits
    ax.set_ylim([-5, 5])  # Set y-axis limits

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node("plotter_xy")
    
    # Subscribe to the lidar_xy topic
    rospy.Subscriber("lidar_xy", ArrayXY, plot_xy)
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Create an animation
    ani = animation.FuncAnimation(fig, update_plot, frames=None, interval=1, save_count=100)
    
    # Show the plot
    plt.show()
    
    # Keep the node running
    rospy.spin()

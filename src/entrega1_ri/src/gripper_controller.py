#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

class GripperController:
    def __init__(self, gripper_topic):
        self.gripper_pub = rospy.Publisher(gripper_topic, Float64, queue_size=10)
        self.current_gripper_position = None

    def control_gripper(self, position):
        if self.current_gripper_position is None or self.current_gripper_position != position:
            msg = Float64()
            msg.data = position
            self.gripper_pub.publish(msg)
            self.current_gripper_position = position
            rospy.loginfo("Gripper position sent: %f", position)

    def wait_for_gripper_change(self, current_position, timeout):
        start_time = rospy.Time.now()
        while not rospy.is_shutdown():
            if self.current_gripper_position != current_position:
                break
            if (rospy.Time.now() - start_time).to_sec() > timeout:
                rospy.logwarn("Timeout waiting for gripper position to change")
                break
            rospy.sleep(0.1)  # Check every 100ms if the gripper position has changed

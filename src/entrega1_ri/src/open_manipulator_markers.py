#!/usr/bin/env python3
import rospy
import tf
from markers import BallMarker, color

class MarkerPublisher:
    def __init__(self):
        self.bmarker_des = BallMarker(color['RED'])
        self.bmarker = BallMarker(color['GREEN'])
        self.bmarker1 = BallMarker(color['BLUE'])
        self.bmarker2 = BallMarker(color['YELLOW'])
        self.listener = tf.TransformListener()
        self.initial_position = [0.286, 0, 0.205]  # Set to the initial position
        self.position1 = [0.286, 0.00, 0.05]  # Additional marker position
        self.position2 = [0.000, 0.28, 0.05]  # Additional marker position

    def get_end_effector_position(self):
        try:
            (trans, rot) = self.listener.lookupTransform('/world', '/end_effector_link', rospy.Time(0))
            return trans
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logerr("Could not get end effector position")
            return None

    def run(self):
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            ee_position = self.get_end_effector_position()
            if ee_position:
                self.bmarker.xyz(self.initial_position)
                self.bmarker_des.xyz(ee_position)
                self.bmarker1.xyz(self.position1)
                self.bmarker2.xyz(self.position2)
                self.bmarker.publish()
                self.bmarker_des.publish()
                self.bmarker1.publish()
                self.bmarker2.publish()
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node("marker_publisher", anonymous=True)
    marker_publisher = MarkerPublisher()
    marker_publisher.run()

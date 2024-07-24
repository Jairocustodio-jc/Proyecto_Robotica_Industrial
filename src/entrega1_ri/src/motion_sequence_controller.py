import rospy

class MotionSequenceController:
    def __init__(self, manipulator_controller, gripper_controller):
        self.manipulator_controller = manipulator_controller
        self.gripper_controller = gripper_controller

    def move_through_sequence(self, positions_sequence):
        for i, pos in enumerate(positions_sequence):
            self.manipulator_controller.move_to_position(pos[0], pos[1], pos[2])
            rospy.sleep(0.2)  
            if i == 0:
                self.gripper_controller.control_gripper(0.01)
                rospy.sleep(0.2)
                self.gripper_controller.control_gripper(-0.005)
                rospy.sleep(0.2)
                self.gripper_controller.wait_for_gripper_change(-0.005, 5)
            elif i == 2:
                self.gripper_controller.control_gripper(0.01)
                rospy.sleep(0.2)
                self.gripper_controller.wait_for_gripper_change(0.01, 5)
            rospy.sleep(0.2)
        self.sequence_completed = True

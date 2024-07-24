cmake_minimum_required(VERSION 3.0.2)
project(entrega1_ri)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  ArrayXY.msg
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES entrega1_ri
  CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

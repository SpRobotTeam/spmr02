cmake_minimum_required(VERSION 2.8.3)
project(spmr02)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  nav_msgs
  geometry_msgs
  tf
  tf2
  actionlib
  actionlib_msgs
)

add_action_files(
  DIRECTORY action
  FILES GoToPose.action
)

catkin_install_python(
    PROGRAMS
        nodes/spmr_controller
        nodes/spmr_go_to_goal
        nodes/spmr_PathFind
        nodes/spmr_canopen

    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

catkin_python_setup()

generate_messages (
  DEPENDENCIES actionlib_msgs std_msgs geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS 
  actionlib_msgs
  rospy
  std_msgs
  nav_msgs
  geometry_msgs
  tf
  tf2
  actionlib
  actionlib_msgs
)

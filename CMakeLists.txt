################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 3.0.2)
project(spmr02)
cmake_policy(SET CMP0054 NEW)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  gazebo_ros
  sensor_msgs
)

find_package(gazebo REQUIRED)

catkin_package(
#   INCLUDE_DIRS include
  CATKIN_DEPENDS roscpp std_msgs gazebo_ros sensor_msgs
  DEPENDS GAZEBO
)

catkin_install_python(PROGRAMS
  nodes/rep117_filter.py
  nodes/spmr_teleop_key
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
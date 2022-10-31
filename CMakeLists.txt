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

generate_messages (
  DEPENDENCIES actionlib_msgs std_msgs geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS
  actionlib
  actionlib_msgs
)

add_action_files(
  DIRECTORY action
  FILES
#   GoToPose.action
)

catkin_package()

find_package(roslaunch)

catkin_install_python(
    PROGRAMS
        # nodes/diff_drive_odometry
        nodes/spmr_controllerpy
        nodes/spmr_go_to_goal.py
        nodes/spmr_PathFind.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})


foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

# generate_messages (
#   DEPENDENCIES actionlib_msgs std_msgs geometry_msgs
# )





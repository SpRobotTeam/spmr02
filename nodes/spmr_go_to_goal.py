#! /usr/bin/env python3
from __future__ import division

import math
import rospy
import std_msgs.msg
from math import pi, asin, acos
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist, PoseStamped, Pose, Point
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Bool


from spmr02.nodes.src import goal_controller
from spmr02.nodes.src import pose


import actionlib
from diff_drive.msg import GoToPoseAction, GoToPoseGoal, GoToPoseResult

class GoToGoalNode:

    def __init__(self):
        self.controller = goal_controller.GoalController()

    def main(self):
        rospy.init_node('diff_drive_go_to_goal')

        self.action_name = 'diff_drive_go_to_goal'
        self.action_server \
            = actionlib.SimpleActionServer(self.action_name, GoToPoseAction,
                                           execute_cb=self.on_execute,
                                           auto_start=False)

        self.action_client = actionlib.SimpleActionClient(
            'diff_drive_go_to_goal', GoToPoseAction)

        self.dist_pub = rospy.Publisher('~distance_to_goal', Float32, queue_size=10)
        self.twist_pub = rospy.Publisher('test_mr/cmd_val', Twist, queue_size=10)
        self.goal_achieved_pub = rospy.Publisher('goal_achieved', Bool, queue_size=1)
        # self.Next_poi = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=1)

        self.node_name = rospy.get_name()
        rospy.loginfo("{0} started".format(self.node_name))

        rospy.Subscriber('odom', Odometry, self.on_odometry)
        rospy.Subscriber('move_base_simple/goal', PoseStamped, self.on_goal)

        rate = rospy.get_param('~rate', 10.0)
        self.rate = rospy.Rate(rate)
        self.dT = 1 / rate

        self.kP = rospy.get_param('~kP', 20.0)  # 3.0 30.0 15.0
        self.kA = rospy.get_param('~kA', 200.0) # 8.0 120.0
        self.kB = rospy.get_param('~kB', -3.0)  #-1.5 -10.5 -50.5 -1.0
        self.controller.set_constants(self.kP, self.kA, self.kB)

        self.controller.set_linear_tolerance(
            rospy.get_param('~linear_tolerance', 0.025))        # 2.5cm
        self.controller.set_angular_tolerance(
            rospy.get_param('~angular_tolerance', 1/180*pi))    # 1 degrees

        self.controller.set_max_linear_speed(
            rospy.get_param('~max_linear_speed', 1.2))
        self.controller.set_min_linear_speed(
            rospy.get_param('~min_linear_speed', 0))
        self.controller.set_max_angular_speed(
            rospy.get_param('~max_angular_speed', 1.0))
        self.controller.set_min_angular_speed(
            rospy.get_param('~min_angular_speed', 0))
        self.controller.set_max_linear_acceleration(
            rospy.get_param('~max_linear_acceleration', 1.1))
        self.controller.set_max_angular_acceleration(
            rospy.get_param('~max_angular_acceleration', 1.3))

        # Set whether to allow movement backward. Backward movement is
        # safe if the robot can avoid obstacles while traveling in
        # reverse. We default to forward movement only since many
        # sensors are front-facing.

        self.controller.set_forward_movement_only(
            rospy.get_param('~forwardMovementOnly', True))

        self.init_pose()
        self.goal = None

        self.action_server.start()

        rospy.spin()

    def on_execute(self, goal):
        self.goal = self.get_angle_pose(goal.pose.pose)
        rospy.loginfo('Goal: (%f,%f,%f)', self.goal.x, self.goal.y,
                      self.goal.theta)

        success = True
        while not rospy.is_shutdown() and self.goal is not None:
        # while not rospy.is_shutdown():
            # Allow client to preempt the goal.
            if self.action_server.is_preempt_requested():
                rospy.loginfo('Goal preempted')
                self.send_velocity(0, 0)
                self.action_server.set_preempted()
                success = False
                break
            self.publish()
            self.rate.sleep()

        result = GoToPoseResult()
        result.success = success
        self.action_server.set_succeeded(result)

    def init_pose(self):
        self.pose = pose.Pose()
        self.pose.x = 0
        self.pose.y = 0
        self.pose.theta = 0

    def publish(self):
        if self.controller.at_goal(self.pose, self.goal):
            desired = pose.Pose()
        else:
            desired = self.controller.get_velocity(self.pose, self.goal,
                                                   self.dT)

        if self.goal is not None \
           and (desired.xVel!=0.0 or desired.thetaVel!=0.0):
            rospy.loginfo(
                'current=(%f,%f,%f) goal=(%f,%f,%f)  xVel=%f thetaVel=%f',
                self.pose.x, self.pose.y, self.pose.theta,
                self.goal.x, self.goal.y, self.goal.theta,
                desired.xVel, desired.thetaVel)

        d = self.controller.get_goal_distance(self.pose, self.goal)
        self.dist_pub.publish(d)

        self.send_velocity(desired.xVel, desired.thetaVel)

        # Forget the goal if achieved.
        if self.controller.at_goal(self.pose, self.goal):
            rospy.loginfo('Goal achieved')
            self.goal = None
            msg = Bool()
            msg.data = True
            self.goal_achieved_pub.publish(msg)
        else:
            rospy.loginfo('Goal going')
            msg = Bool()
            msg.data = False
            self.goal_achieved_pub.publish(msg)
        

    def send_velocity(self, xVel, thetaVel):
        twist = Twist()
        twist.linear.x = xVel
        twist.angular.z = thetaVel
        self.twist_pub.publish(twist)

    def on_odometry(self, newPose):
        self.pose = self.get_angle_pose(newPose.pose.pose)

    def on_goal(self, goal):
        self.action_client.wait_for_server()
        action_goal = GoToPoseGoal()
        action_goal.pose.pose = goal.pose
        self.action_client.send_goal(action_goal)

    def get_angle_pose(self, quaternion_pose):
        q = [quaternion_pose.orientation.x,
             quaternion_pose.orientation.y,
             quaternion_pose.orientation.z,
             quaternion_pose.orientation.w]
        roll, pitch, yaw = euler_from_quaternion(q)
        # print("yaw :", yaw)

        angle_pose = pose.Pose()
        angle_pose.x = quaternion_pose.position.x
        angle_pose.y = quaternion_pose.position.y
        angle_pose.theta = yaw
        return angle_pose

if __name__ == '__main__':
    try:
        node = GoToGoalNode()
        node.main()
    except rospy.ROSInterruptException:
        pass

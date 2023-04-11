import rospy
from sensor_msgs.msg import JointState

rospy.init_node('joint_state_publisher')
joint_pub = rospy.Publisher('joint_states', JointState, queue_size=10)
rate = rospy.Rate(30)

rospy.Subscriber("lwheel_position", Twist, self.twistCallback)
rospy.Subscriber("rwheel_position", Twist, self.twistCallback)

while not rospy.is_shutdown():
    joint_state = JointState()
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name.append("left_wheel_joint")
    joint_state.position.append(0.0)
    joint_state.velocity.append(0.0)
    joint_state.effort.append(0.0)

    joint_state.name.append("right_wheel_joint")
    joint_state.position.append(0.0)
    joint_state.velocity.append(0.0)
    joint_state.effort.append(0.0)

    joint_pub.publish(joint_state)
    rate.sleep()
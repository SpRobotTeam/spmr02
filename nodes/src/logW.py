import rospy

def log_write(log_data):
    log = open("/home/tang/catkin_ws/src/diff_drive/plot/d.txt", 'a')
    log.write(log_data)
    log.close
    return

# log = "{0} {1}".format(rospy.get_time(),msg.data)
# log_write(log)

# log.log_write("{0} {1}".format(rospy.get_time(),msg.data))
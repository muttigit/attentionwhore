#!/usr/bin/env python
import roslib; roslib.load_manifest('attentionwhore')
import rospy
#from std_msgs.msg import String
#from std_msgs.msg import UInt16MultiArray
from attentionwhore.msg import Trajectory


def callback(data):
    #rospy.loginfo(data.data)
    rospy.loginfo(data)


def listener():
    rospy.init_node('ik_solver_listener', anonymous=True)
    #rospy.Subscriber("/string", String, callback)
    rospy.Subscriber("/trajectory", Trajectory, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

#!/usr/bin/env python
import roslib; roslib.load_manifest('attentionwhore')
import rospy
from std_msgs.msg import String


def talker():
    pub = rospy.Publisher('/string', String)
    rospy.init_node('ik_solver_talker')
    msg = String("Fernando")
    while not rospy.is_shutdown():
        #msg.message = str(raw_input(msg.nickname + ": "))
        #rospy.loginfo(msg)
        pub.publish(msg)
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

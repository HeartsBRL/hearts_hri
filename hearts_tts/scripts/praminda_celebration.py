#!/usr/bin/env python


import rospy
import time
from std_msgs.msg import String

pub_motion =        rospy.Publisher("motion_name", String, queue_size=10)
tts_pub =           rospy.Publisher("/hearts/tts", String, queue_size=10)


rospy.init_node("praminda_celeb")
rospy.sleep(1)

msg = String()
msg.data = "I may not have emotions, but the people who programmed me do, and they are very proud of you. Well done."
tts_pub.publish(msg)

motion = String()
motion.data = "give_receive"
pub_motion.publish(motion)

rospy.sleep(6)

motion.data = "open_gripper"
pub_motion.publish(motion)

rospy.sleep(4)
motion.data = "hold_close"
pub_motion.publish(motion)

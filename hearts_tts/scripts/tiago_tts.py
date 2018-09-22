#!/usr/bin/env python


import sys
import rospy
from actionlib import SimpleActionClient
from pal_interaction_msgs.msg import TtsAction, TtsGoal
from std_msgs.msg import String


def talk_to_me(words):
    #creates the ts goal and sends it off to be spoken
    ttg = TtsGoal()
    ttg.rawtext.text = words.data
    ttg.rawtext.lang_id = "en_GB"
    client.send_goal_and_wait(ttg)

#start the node
rospy.init_node('tiago_tts')

# Connect to the text-to-speech action server
client = SimpleActionClient('/tts', TtsAction)
client.wait_for_server()
#Subscribe to get what we want to say
rospy.Subscriber('/hearts/tts', String, talk_to_me)

rospy.spin()


#if __name__ == '__main__':

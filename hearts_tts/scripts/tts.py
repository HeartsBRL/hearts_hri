#!/usr/bin/python
import rospy
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import alsaaudio # added 26/02/2017 in Edinburgh
import time

mixer_spk = alsaaudio.Mixer(control='Master', id=0)
mixer_mic = alsaaudio.Mixer(control='Capture', id=0) 


def callback(data):
    mixer_spk.setmute(0)
    mixer_mic.setrec(0)
  
    lstr = len(data.data)

    soundhandle.say(data.data)
    delay = lstr * 0.125
    time.sleep(delay)


    mixer_mic.setrec(1)
    mixer_spk.setmute(1)

    print("tts - is finished for: " + data.data)

    return

soundhandle = SoundClient()
rospy.init_node("tts",anonymous=True)
rospy.Subscriber("/hearts/tts", String, callback)
rospy.spin()

#!/usr/bin/python
####################################################################
# derek 14 Feb 2019 - adjust to just say what it is told. Mic now 
#                    handled in generic controller  by toggle_sst
#####################################################################
import rospy
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import alsaaudio # added 26/02/2017 in Edinburgh
import time

mixer_spk = alsaaudio.Mixer(control='Master', id=0)
#mixer_mic = alsaaudio.Mixer(control='Capture', id=0)

#print("\n###### check alsaaudio is loaded #####\n")
#p = alsaaudio.__file__
#print("alsaaudio module path is:\n"+p+"\n")

def callback(data):
    mixer_spk.setmute(0)
    #mixer_mic.setrec(0)

    lstr = len(data.data)
   
    soundhandle.say(data.data)
  
    #delay = lstr * 0.125
    #time.sleep(delay)


    #mixer_mic.setrec(1)
    # dont switch speaker off -  as stt_togge should now not listen 
    # when text is being spoken by the robot
    # mixer_spk.setmute(1)

    #print("tts - is finished for: " + data.data)

    return

soundhandle = SoundClient()
rospy.init_node("tts",anonymous=True)
rospy.Subscriber("/hearts/tts", String, callback)
rospy.spin()

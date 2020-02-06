#!/usr/bin/python
####################################################################
# Derek 06 Feb 2020 - toggle_stt now controls subscribers for speak
#                     back. tts listens continuously now.
#                     NB TBM3 does not use generic contoller toggle_stt
#                     but a similar approach of it's own inside TBM3.
#                     WE  use to estmimate time taken by speech bt
#                     now publish to topic "tts_finished". Also
#                     "blocking=True" introduced as this seems t
#                     make sund play to the end rather than  stopping
#                     prematurely. 
####################################################################
# derek 14 Feb 2019 - adjust to just say what it is told. Mic now 
#                    handled in generic controller  by toggle_sst
####################################################################

import rospy
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import alsaaudio # added 26/02/2018 in Edinburgh
import time

mixer_spk = alsaaudio.Mixer(control='Master', id=0)
#mixer_mic = alsaaudio.Mixer(control='Capture', id=0)

#print("\n###### check alsaaudio is loaded #####\n")
#p = alsaaudio.__file__
#print("alsaaudio module path is:\n"+p+"\n")

def callback(data):
    print("***TTS: in tts callback #####")
    mixer_spk.setmute(0)
    #mixer_mic.setrec(0)

    #lstr = len(data.data)
    #print("***TTS: BEfore soundhandle")
    soundhandle.say(data.data,blocking=True)
    #soundhandle.say(data.data)
    #print("***TTS: AFTER  soundhandle")
    #rospy.sleep(0.5)

    pub_tts_finished.publish("tts_finished") 

    #delay = lstr * 0.1
    #time.sleep(delay)


    #mixer_mic.setrec(1)
    # dont switch speaker off -  as stt_togge should now not listen 
    # when text is being spoken by the robot
    # mixer_spk.setmute(1)

    #print("tts - is finished for: " + data.data)

    return


pub_tts_finished = rospy.Publisher("/hearts/tts_finished", String, queue_size = 10)
soundhandle = SoundClient()
rospy.init_node("tts",anonymous=True)
rospy.Subscriber("/hearts/tts", String, callback)
rospy.spin()

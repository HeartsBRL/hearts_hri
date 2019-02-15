# Filename: gcp_keywords_r.py
# Created: 25 OCT 2017
# Author : Derek Ripper
# Purpose: Define list of keywords/phrases that can be used in
#          the google_cloud speech recognition in stt.py to be 
#          used as the "preferred_phrases"  
#
#          List to be read from text file as defined in ROS param
################################################################################
# Updates:
#
# 14 Nov 2018 Derek - added module "text_colours" to support colour printing to screen
################################################################################

import rospy
import os
import python_support_library.text_colours     as TC      # print text in various colour styles

prt = TC.tc()

def gcp_keywords_r():



# get file name for keywords/phrases
    GCPKEYWORDSFILE  = rospy.get_param("SR_GCP_KEYWORDSFILE")

# check taht a file exists
    if os.path.isfile(GCPKEYWORDSFILE):
    
# read into a list of keywords/phrases
        with open(GCPKEYWORDSFILE, "r") as fh: 
            preferred_phrases = fh.read().splitlines()         
    else:

        preferred_phrases = []
        prt.warning("*** WARNING - NO GCP KEYWORDS file was found!")
        prt.warning("*** for File name: "+ GCPKEYWORDSFILE)

    prt.info("*** Number of GCP preferred_phrases found: "+str(len(preferred_phrases)))
    return preferred_phrases

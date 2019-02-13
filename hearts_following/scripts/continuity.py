#!/usr/bin/env python

#This file is intended to keep track of an individual object amongst
#other similar objects by analysing continuity in location data

import rospy
import math
import tf 
from std_msgs.msg import Float64, Int16
from geometry_msgs.msg import Point, PointStamped, Quaternion, PoseStamped

from hearts_follow_msgs.msg import Points, ConPoint


class Continuity():

    def __init__(self):
        #subscribers
        self.sub_poses = rospy.Subscriber("hearts/follow_candidates", Points, self.measure_continuity)
        
        #publishers
        self.pub_best = rospy.Publisher("hearts/navigation/goal_shortcut", PoseStamped, queue_size=1)
        
        self.pub_obj_detect = rospy.Publisher("hearts/obj_on", Int16, queue_size=1)
        
        #transform listener for conversion to real-world coords
        self.listener = tf.TransformListener()
        
        #init vars
        self.last_known = PointStamped()
        self.last_known.point.x = 0
        self.last_known.point.y = 0
        self.last_known.point.z = 0
        self.last_known.header.frame_id = "map"


    def point_distance(self, p1, p2):
        x1 = p1.x
        y1 = p1.y
        z1 = p1.z
        x2 = p2.x
        y2 = p2.y
        z2 = p2.z
        #sqrt(x^2 + y^2 + z^2) = distance
        dist = math.sqrt( ((x1-x2)**2) + ((y1-y2)**2) + ((z1-z2)**2) )
        return dist


    # for now, continuity is just distance from last known location
    #TODO implement more robust contuinuity such as gradients & fitting
    def measure_continuity(self, points):
        length = len(points)
        best_dist = 99999999
        best_index = 0
        # Loop through finding distance for each point
        for x in range(0,length):
            dist = point_distance(points[x].point, last_known.point)
            points[x].continuity = dist
            #if this is the best so far, make note of it
            if dist < best_dist:
                best_dist = dist
                best_index = x
                
        #find tiago's position & orientation in map coords
        (pos,ori) = listener.lookupTransform("/map","/base_footprint",rospy.Time())
        #create PointStamped message to save as last known location and publish for other nodes to use
        msg = PoseStamped()
        bestpoint = points[best_index].point
        msg.position.x = bestpoint.x
        msg.position.y = bestpoint.y
        msg.position.z = bestpoint.z
        msg.orientation = ori
        msg.header.frame_id = "xtion_rgb_optical_frame"
        self.last_known.point = bestpoint
        self.pub_best.publish(msg)
            
    # not actually used currently, delete?     
    def set_last_location(self, point):
        self.last_known.x = point.x
        self.last_known.y = point.y
        self.last_known.z = point.z
        self.last_known.header.frame_id = self.strip_leading_slash(point.header.frame_id)


#Main
if __name__ == '__main__':
    rospy.init_node("continuity_measure")
    continuity_instance = Continuity()
    #msg = Int()
    #msg.data = 1
    #self.pub_obj_detect.publish(msg)
    rospy.spin()


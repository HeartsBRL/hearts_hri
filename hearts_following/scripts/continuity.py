#!/usr/bin/env python

#This file is intended to keep track of an individual object amongst
#other similar objects by analysing continuity in location data

import rospy
import math
import tf
from std_msgs.msg import Float64, Int16, String
from geometry_msgs.msg import Point, PointStamped, Quaternion, PoseStamped, Pose2D


from hearts_follow_msgs.msg import Points, ConPoint


class Continuity:

    def __init__(self):
        #subscribers
        #self.sub_poses = rospy.Subscriber("hearts/follow_candidates", Points, self.measure_continuity)
        self.sub_follow_toggle = rospy.Subscriber("hearts/follow_toggle", Bool, status)


        #publishers
        self.pub_best = rospy.Publisher("hearts/navigation/goal", Pose2D, queue_size=1)
        self.clear_movement = rospy.Publisher("hearts/navigation/stop", String, queue_size=1)
        #self.pub_obj_detect = rospy.Publisher("hearts/obj_on", Int16, queue_size=1)


        #transform listener for conversion to real-world coords
        self.listener = tf.TransformListener()

        #init vars
        self.last_known = PointStamped()
        self.last_known.point.x = 0
        self.last_known.point.y = 0
        self.last_known.point.z = 0
        self.last_known.header.frame_id = "xtion_rgb_optical_frame"

    def toggle_callback(self):
        ''' Listens to the output of the follow_toggle topic and initiates following by subscribing to SOMETHING that starts the whole process'''
        if self.sub_follow_toggle is True:
            print("***** START following *****")
            self.sub_poses = rospy.Subscriber("hearts/follow_candidates", Points, self.measure_continuity) #TODO check this is the right one







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
    def measure_continuity(self, things):
        length = len(things.points)
        best_dist = 99999999
        best_index = 0
        # Loop through finding distance for each point
        for x in range(0,length):
            dist = self.point_distance(things.points[x].point, self.last_known.point)
            things.points[x].continuity = dist
            #if this is the best so far, make note of it
            if dist < best_dist:
                best_dist = dist
                best_index = x

        #find tiago's position & orientation in map coords

        #create PointStamped message to save as last known location and publish for other nodes to use
        msg = PointStamped()
        goal = PointStamped()
        print(best_index)
        bestpoint = things.points[best_index]
        msg.point.x = bestpoint.point.x
        msg.point.y = bestpoint.point.y
        msg.point.z = bestpoint.point.z
        #msg.pose.orientation = ori
        msg.header.frame_id = "xtion_rgb_optical_frame"

        angle = math.atan2(msg.point.z,msg.point.y)
        if angle > math.pi:
            angle = -(math.pi - angle)
        #print(msg)
        goal = self.listener.transformPoint("map", msg)

        (pos,ori) = self.listener.lookupTransform("/base_footprint","/map",rospy.Time())
        twoD = Pose2D()
        twoD.x = goal.point.x
        twoD.y = goal.point.y
        euler = tf.transformations.euler_from_quaternion(ori)
        twoD.theta = euler[2] + angle
        print(twoD)
        self.last_known.point = bestpoint.point
        stop = String()
        stop.data = "Stop"
        self.clear_movement.publish(stop)
        rospy.sleep(0.01)
        self.pub_best.publish(twoD)


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

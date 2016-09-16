#!/usr/bin/env python
# import roslib
# roslib.load_manifest('~/ros-workspaces/hackathon_ws/src/hackathon_project/package.xml')

# ROS imports:
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point

# Python imports:
import sys
import rospy
import cv2
import numpy as np
import trackbar as tb
from cv_bridge import CvBridge, CvBridgeError
from collections import deque



pts = deque(maxlen=32)

class image_converter:
    def __init__(self):
        self.pos_mot_0 = 0x7A
        self.pos_mot_1 = 0x7A

        self.image_pub = rospy.Publisher("image_topic_2", Image, queue_size=10)
        self.mot_pub = rospy.Publisher("motor_commands", Point, queue_size=10)
        #rate = rospy.Rate(3) # 10hz

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

        # create trackbars for color change
        win = cv2.namedWindow("MyImage")
        name = "MyImage"
        cv2.createTrackbar('H_low',name,0,255,tb.nothing)
        cv2.createTrackbar('S_low',name,164,255,tb.nothing)
        cv2.createTrackbar('V_low',name,80,255,tb.nothing)
        cv2.createTrackbar('H_high',name,180,255,tb.nothing)
        cv2.createTrackbar('S_high',name,220,255,tb.nothing)
        cv2.createTrackbar('V_high',name,255,255,tb.nothing)

    def moto_logic(self, center):
        # use the center of the ball and camera to make direction and move that way
        newCenter = np.array([center[0], center[1]])
        screenCenter = np.array([640*0.5, 480*0.5])
        distDir = newCenter - screenCenter
        #distDir = distDir/np.linalg.norm(distDir)
        #if distDir[0] < 1:
        if abs(distDir[0]) > 0:
            self.pos_mot_0 += 0.1 * distDir[0]/abs(distDir[0])
        # else:
        #     self.pos_mot_0 += distDir[0]

        #if distDir[1] < 1:
        if abs(distDir[1]) > 0:
            self.pos_mot_1 += 0.1 * distDir[1]/abs(distDir[1])
        # else:
        #     self.pos_mot_1 += distDir[1]

        # clip motor positions and within boundaries if necessary
        if self.pos_mot_0 < 1:
            self.pos_mot_0 = 1
        elif self.pos_mot_0 > 254:
            self.pos_mot_0 = 254
        if self.pos_mot_1 < 1:
            self.pos_mot_1 = 1
        elif self.pos_mot_1 > 254:
            self.pos_mot_1 = 254
        #put values in msg type and publish
        out = Point()
        out.x = self.pos_mot_0
        out.y = self.pos_mot_1
        out.z = 0
        rospy.loginfo(out)
        self.mot_pub.publish(out)

    def callback(self,data):
        try:
            imgOriginal = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print("==[CAMERA MANAGER]==", e)

        blurred = cv2.GaussianBlur(imgOriginal,(11,11),0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        h_low,s_low,v_low,h_hi,s_hi,v_hi = tb.trackbar("MyImage",imgOriginal)

        lower = np.array([h_low,s_low,v_low])
        upper = np.array([h_hi,s_hi,v_hi])
    	mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=7)
        mask = cv2.dilate(mask, None, iterations=7)
        output = cv2.bitwise_and(imgOriginal, imgOriginal, mask = mask)
        outputGrayscale = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        contours = cv2.findContours(outputGrayscale,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

        if len(contours) > 0:
            c = max(contours,key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                #send message
                self.moto_logic(center)

                #draw
                cv2.circle(imgOriginal,(int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(imgOriginal,center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
                for i in np.arange(1,len(pts)):
                    thickness = int(np.sqrt(32/float(i+1))*2.5)
                    cv2.line(imgOriginal,pts[i-1],pts[i],(0,0,255),thickness)

        flipped = cv2.flip(imgOriginal, 1)
        cv2.imshow("Image", flipped)
        cv2.imshow("MyImage", output)
        cv2.waitKey(3)

def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

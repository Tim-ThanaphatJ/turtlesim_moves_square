#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import numpy as np

is_init_pose = False
is_init_degree = False
turnCCW = False

initPose = []
currentPose = []

turtleVelX = 0.75
turtleAngZ = 0.5

squareDist = 2.0
status = ""

def poseReceived(position_data): #callback
    global currentPose  
    currentPose = [position_data.x, position_data.y, position_data.theta]

def moveSquare(polygon):

    angleDegree = 360//polygon #degree
    angleRadius = (angleDegree * 2 * np.pi)/360

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseReceived)

    turtleVel = Twist()

    rospy.init_node('moveSquare4turtleSim', anonymous=False)
    rate = rospy.Rate(20) # 20hz

    while not rospy.is_shutdown():
        global initPose, turnCCW, is_init_pose, status
        if turnCCW == False:
            if is_init_pose == False:
                initPose = currentPose
                is_init_pose = True
            else:
                dist = np.sqrt(np.power((currentPose[0] - initPose[0]), 2) + np.power((currentPose[1] - initPose[1]), 2))

                if dist >= squareDist:
                    turtleVel.linear.x = 0
                    turnCCW = True
                    is_init_pose = False
                else:
                    turtleVel.linear.x = turtleVelX
                    status = "Going Forward: " + str(dist)
        else:
            if(currentPose[2] < 0):
                currentPose[2] = (np.pi*2) - np.abs(currentPose[2])
            if(initPose[2] < 0):
                initPose[2] = (np.pi*2) - np.abs(initPose[2])
                
            angleDiff = np.abs((currentPose[2]) - (initPose[2]))
            status = "Turning: " + str((angleDiff*180)/np.pi) + " degree"

            if angleDiff >= angleRadius:
                turtleVel.angular.z = 0
                turnCCW = False
            else:
                turtleVel.angular.z = turtleAngZ

        velocity_publisher.publish(turtleVel)

        rospy.loginfo(status)
        rate.sleep()

if __name__ == '__main__':
    try:
        moveSquare(4)
    except rospy.ROSInterruptException:
        pass
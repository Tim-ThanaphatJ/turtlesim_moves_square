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

turtleVelX = 0.5
turtleAngZ = 0.25

squareDist = 2.0
angleDegree = 90.0
angleRadius = (angleDegree * 2 * np.pi)/360

def poseReceived(position_data): #callback
    global currentPose  
    currentPose = [position_data.x, position_data.y, position_data.theta]

def moveSquare():
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseReceived)

    turtleVel = Twist()

    rospy.init_node('moveSquare4turtleSim', anonymous=False)
    rate = rospy.Rate(20) # 20hz

    while not rospy.is_shutdown():
        global initPose, turnCCW, is_init_pose
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
        else:
            angleDiff = np.abs(currentPose[2] - initPose[2])
            if angleDiff >= angleRadius:
                turtleVel.angular.z = 0
                turnCCW = False
            else:
                turtleVel.angular.z = turtleAngZ

        velocity_publisher.publish(turtleVel)

        status = "current: " + str(currentPose) + "action: " + str(turnCCW)
        rospy.loginfo(status)
        rate.sleep()

if __name__ == '__main__':
    try:
        moveSquare()
    except rospy.ROSInterruptException:
        pass
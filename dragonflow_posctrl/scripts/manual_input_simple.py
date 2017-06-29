#!/usr/bin/env python2.7
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Test cde to input positions by hand, and the publish them for the pos_command_in.py node
## using /mavros/setpoint_position/local tpoic
## Created by Thierry Bujard: t.bujard@gmail.com

import time
import rospy
from geometry_msgs.msg import Pose
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool

playground_x_size = 3 #assumes a coordinate center at the center of a rectangle
playground_y_size = 1.5
playground_z_size = 1.3
armed = False

def callback(state):
    global armed
    armed = state.armed

def manual_input():
    rospy.Subscriber('/mavros/state', State, callback)


    input_position = Pose() #creating the position variable, which is of type Pose
    input_pub = rospy.Publisher('manual_pos_input', Pose, queue_size=10) #identifying the message
    rospy.init_node('manual_input', anonymous=False) #wwe don't 
    rate = rospy.Rate(1) # Very slow loop time to allow input

    while not rospy.is_shutdown() :
        valid = True

        while not (armed and valid) :
            arm = raw_input("Arm vehicle? (y)")
            try:
                arm = str(arm)
                pass
            except ValueError:
                print("Enter y or n please!")
                valid = False
                continue
            else:
                if arm == 'y':
                    arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool, 10)
                    arming(True)
                    valid = True
                    time.sleep(2)
                    pass
                else:
                    valid = False


        valid = False
        while not valid:
            coordinate = raw_input("""Input position x (m) : """)
            try:
                input_position.position.x = input_position.position.x + float(coordinate)
                pass
            except ValueError:
                valid = False
                print("""Enter a number please!""")
                continue
            if abs(input_position.position.x) > playground_x_size/2 :
                print("""Enter a number smaller than {0} m""".format(playground_x_size/2))
                valid = False
                pass
            else:
                print("""x target = {0}""".format(coordinate))
                valid = True

        valid = False
        while not valid:
            coordinate = raw_input("""Input position y (m) : """)
            try:
                input_position.position.y = input_position.position.y + float(coordinate)
                pass
            except ValueError:
                valid = False
                print("""Enter a number please!""")
                continue
            if abs(input_position.position.y) > playground_y_size/2 :
                print("""Enter a number smaller than {0} m""".format(playground_y_size/2))
                valid = False
                pass
            else:
                print("""y target = {0}""".format(coordinate))
                valid = True

        valid = False
        while not valid:
            coordinate = raw_input("""Input position z (m) : """)
            try:
                input_position.position.z = input_position.position.z + float(coordinate)
                pass
            except ValueError:
                valid = False
                print("""Enter a number please!""")
                continue
            if abs(input_position.position.z) > playground_z_size or input_position.position.z < 0 :
                print("""Enter a positive number smaller than {0} m""".format(playground_z_size))
                valid = False
                pass
            else:
                print("""z target = {0}""".format(coordinate))
                valid = True

        input_position.orientation.x = 0
        input_position.orientation.y = 0
        input_position.orientation.z = 0

        input_position.orientation.w = -1


        input_pub.publish(input_position) #publish the position
        print("""Position commands sent!""")


        rate.sleep() #enables the rate defined above.

if __name__ == '__main__':
    try:
        manual_input()
    except rospy.ROSInterruptException:
        pass
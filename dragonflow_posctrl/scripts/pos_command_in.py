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

## Code to send position commands to the drone
## using /mavros/setpoint_position/local topic
## Created by Thierry Bujard: t.bujard@gmail.com


import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

x_in = 0.0
y_in = 0.0
z_in = 0.5

qx_in = 0.0
qy_in = 0.0
qz_in = 0.0
qw_in = 1


def callback(input_pos):

    global x_in #globals so that they update also outside of the callback() function
    global y_in
    global z_in
    global qx_in
    global qy_in
    global qz_in
    global qw_in


    x_in = input_pos.position.x #updating the values
    y_in = input_pos.position.y
    z_in = input_pos.position.z

    qx_in = input_pos.orientation.x
    qy_in = input_pos.orientation.y
    qz_in = input_pos.orientation.z
    qw_in = input_pos.orientation.w




def pos_command():

    rospy.Subscriber('manual_pos_input', Pose, callback)

    position = PoseStamped() #creating the position variable, which is of type PoseStamped
    command_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10) #identifying the message
    rospy.init_node('pos_command_in', anonymous=False) #wwe don't 
    rate = rospy.Rate(10) # 2hz is minimal to avoid the PX4 timeout
    while not rospy.is_shutdown():

        position.header.stamp = rospy.Time.now() #timessamp
        position.header.frame_id = "world" #for global coordinate frame. Check what comes out of mocap


        position.pose.position.x = x_in
        position.pose.position.y = y_in
        position.pose.position.z = z_in 
        position.pose.orientation.x = qx_in
        position.pose.orientation.y = qy_in
        position.pose.orientation.z = qz_in
        position.pose.orientation.w = qw_in #Using the updated values when available
        command_pub.publish(position) #publish the position
        print("""   """)
        print("""Sending commands...""")
        command_pub.publish(position) #publish the position
        print("""Position sent:   """)
        print("""    x = {0}""".format(x_in))
        print("""    y = {0}""".format(y_in))
        print("""    z = {0}""".format(z_in))
        print("""Orentation sent:   """)
        print("""    x = {0}""".format(qx_in))
        print("""    y = {0}""".format(qy_in))
        print("""    z = {0}""".format(qz_in))
        print("""    w = {0}""".format(qw_in))

        rate.sleep() #enables the rate defined above.

if __name__ == '__main__':
    try:
        pos_command()
    except rospy.ROSInterruptException:
        pass
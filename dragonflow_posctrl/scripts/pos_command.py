#!/usr/bin/env python
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

## Test cde to send position commands to the drone
## using /mavros/setpoint_position/local tpoic


import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


def pos_command():
    position = PoseStamped() #creating the position variable, which is of type PoseStamped
    command_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10) #identifying the message
    rospy.init_node('pos_command', anonymous=False) #wwe don't 
    rate = rospy.Rate(10) # 2hz is minimal to avoid the PX4 timeout
    while not rospy.is_shutdown():

        position.header.stamp = rospy.Time.now() #timessamp
        position.header.frame_id = "world" #for global coordinate frame. Check what comes out of mocap


        position.pose.position.x = 0.0
        position.pose.position.y = 0.0
        position.pose.position.z = 0.5 #test coordinates for first run
        position.pose.orientation.x = 0
        position.pose.orientation.y = 0
        position.pose.orientation.w = 1 #Zero orientation
        command_pub.publish(position) #publish the position
        rate.sleep() #enables the rate defined above.

if __name__ == '__main__':
    try:
        pos_command()
    except rospy.ROSInterruptException:
        pass
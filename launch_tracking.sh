#!/bin/bash
#This script launches all the nodes needed to do drone position control using ROS.
#It requires the following ROS packages:
# -MAVROS
# -vrpn_client_ros
# -dragonflow_posctrl  (homebrew)

#Note: nodes run in individual terminal windows. 
#The 'gnome-terminal -e "<command>" opens a new terminal running '<command>'.

#This code is under the BSD license.

#Created by Thierry Bujard. t.bujard@gmail.com
 
#Source the files for ROS (in order to have all packages activated)
source /opt/ros/kinetic/setup.bash
source $HOME/catkin_ws/devel/setup.bash #our package is here
echo "Launching ROS core services"
#launch the basic ROS services such as topics servers and param servers
gnome-terminal -e "roscore" 
sleep 3 #we need the sleep to make sure the core is fully started.
#launch the VRPN client made for ROS (This will also launch ROSCORE)
#default port is defined in sample.launch as 3883, the same as in Motive.
echo "Launching VRPN server..."
gnome-terminal -e "roslaunch vrpn_client_ros sample.launch server:=192.168.1.148" #the latter is the server address
sleep 3
echo "Launching relay node"
#This relays the message. However the name ot the vrpn topic is not flexible and dependant from the name of the tracker. Therefore, one has to call the drone object "Drone" in motive. Making this automated would be good.
gnome-terminal -e "rosrun topic_tools relay /vrpn_client_node/Drone/pose /mavros/mocap/pose " 
sleep 3
#launch mavros for PX4 using the wifi connection to communicate
echo "Launching MAVROS"
gnome-terminal -e "roslaunch mavros px4.launch fcu_url:="udp://:14550@192.168.4.1:14555" gcs_url:="udp://@192.168.4.2:14556" " #1st: PixRacer IP, 2nd: Computer IP. The ports are default.
sleep 3
echo "Launching command node"
#This node streams positions at a define rate of around 10Hz. 
#Every time the manual_input node publishes, this node updates its streaming.
gnome-terminal -e "rosrun dragonflow_posctrl pos_command_in.py"
echo "Launching input node"
#This node prompts the user to input position setpoints in  terminal window.
gnome-terminal -e "rosrun dragonflow_posctrl manual_input_simple.py"
echo "Echoing mocap position"
#The 'rostopic echo' command is used to listen to topics
gnome-terminal -e "rostopic echo /mavros/mocap/pose" #opens a terminal that shows the pose sent by the mocap
echo "Echoing drone position"
#Comparing the above with this and making sure it is identical (or crose to the third digit) is crucial.
gnome-terminal -e "rostopic echo /mavros/local_position/pose" #opens a terminal that shows the position as percieved by the drone. 







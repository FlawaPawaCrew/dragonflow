# dragonflow
This Git contains some code working with ROS, MAVROS and PX4 in order to fly a drone using MoCap data coming from an external VRPN server. The setup was made for a PixRacer connected via Wi-Fi, and Optitrack's Motive as  MoCap.y

Requested:
- ROS kinetic
- MAVROS
- vrpn_client_ROS

Installation:
- Clone the dragonflow_posctrl directory in ~/catkin_ws/src
- In /catkin_ws, run $catkin_make

- copy launch tracking.sh wherever you want.

Usage
- run $bash /<'path'>/<'to'>'/<'file'>/launch_tracking.sh
- You might have to change a few things in this script, especially:
  - VRPN server IP address.
  - Arguments for px4.launch concerning communication means.
  - Tracker name in the relay node topic names.

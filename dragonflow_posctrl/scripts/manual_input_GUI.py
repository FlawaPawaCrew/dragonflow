#!/home/thierry/anaconda2/bin/ python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:40:51 2017

@author: Guillaume & Thierry
"""

import sys
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication, QPushButton,
                            QVBoxLayout, QFormLayout, QLineEdit, QLabel)
#import rospy
from geometry_msgs.msg import Pose

class manual_input(QWidget):
    
    def __init__(self):
        super(manual_input, self).__init__()
        
        
        #define variable
        input_position = Pose() #creating the position variable, which is of type Pose
        
        #Define ROS node
        input_pub = rospy.Publisher('manual_pos_input', Pose, queue_size=10) #identifying the message
        #rospy.init_node('manual_input', anonymous=False) #wwe don't 
        #rate = rospy.Rate(0.1) # Very slow loop time to allow input
        
        #Create layouts
        self.v_layout = QVBoxLayout() 
        self.f_layout = QFormLayout()
        
        
        
        
        # Create instances of PyQt Widgets, such as buttons
        self.pb_arm = QPushButton("Arm")
        self.pb_arm.clicked.connect(self.pb_arm_clicked)
        
        self.pb_publish = QPushButton("Publish")
        self.pb_publish.clicked.connect(self.pb_publish_clicked)
        
        self.le_lineEditx = QLineEdit("0")
        self.le_lineEdity = QLineEdit("0")
        self.le_lineEditz = QLineEdit("0.5")
        self.le_lineEditqz = QLineEdit("0")
        
        # Layout Management
        self.v_layout.addWidget(self.pb_arm)
        self.v_layout.addWidget(self.pb_publish)


        self.f_layout.addRow(QLabel("x: "), self.le_lineEditx)
        self.f_layout.addRow(QLabel("y: "), self.le_lineEdity)
        self.f_layout.addRow(QLabel("z: "), self.le_lineEditz)
        
        self.v_layout.addLayout(self.f_layout)
        
        
        self.setLayout(self.v_layout)
        self.initUI()
        
        #rate.sleep() #enables the rate defined above.
        
    def pb_arm_clicked(self):
        print self.le_lineEditx.text()
        
    def pb_publish_clicked(self):
        x_in = self.le_lineEditx.text()
        try:
            input_position.position.x = float(x_in)
        except ValueError:
            input_position.position.x = 0
            
        y_in = self.le_lineEdity.text()
        try:
            input_position.position.y = float(y_in)
        except ValueError:
            input_position.position.y = 0
            
            
        z_in = self.le_lineEditz.text()
        try:
            input_position.position.z = float(z_in)
        except ValueError:
            input_position.position.z = 0.5
            
        print input_position.position.x
        print input_position.position.y
        print input_position.position.z
            
            
            
    def initUI(self):               
        
        self.resize(250, 150)
        self.center()
        
        self.setWindowTitle('Manual position input')    
        self.show()
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    ex = manual_input()
    sys.exit(app.exec_())  
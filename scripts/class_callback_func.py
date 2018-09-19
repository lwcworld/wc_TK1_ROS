#!/usr/bin/env python
import numpy as np
import math
import rospy
from std_msgs.msg import Header

from tf.transformations import quaternion_from_euler, euler_from_quaternion

from threading import Thread, Event

# msgs
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import OverrideRCIn, State, Thrust, AttitudeTarget
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped, Quaternion, Pose, PoseWithCovarianceStamped
from sensor_msgs.msg import NavSatFix, Imu
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState

from coordinate_transform import *
from own_publisher import *

class cb():
    def __init__(self):
        self.state = PoseStamped() # state of UAV : position related info
        self.status = State() # status of UAV : flight status info (arm/disarm, mode, etc..)
        self.imu_data = Imu
        self.imu_data_raw = Imu

        self.x_m = 0
        self.y_m = 0
        self.z_m = 0

        self.ax_m = 0
        self.ay_m = 0
        self.az_m = 0

        self.p_m = 0 # angular x velocity
        self.q_m = 0 # angular y velocity
        self.r_m = 0 # angular z velocity

        self.lat_ref = 0
        self.lon_ref = 0
        self.alt_ref = 0

    def local_position_callback(self, msg):
        self.state = msg

    def uav_state_callback(self, msg):
        self.status = msg

    def imu_data_callback(self, msg): # fused data (raw data + computed from FCU)
        # print(msg)
        self.imu_data = msg

    def imu_data_raw_callback(self, msg): # raw data
        self.imu_data_raw = msg

        self.ax_m = self.imu_data_raw.linear_acceleration.x
        self.ay_m = self.imu_data_raw.linear_acceleration.y
        self.az_m = self.imu_data_raw.linear_acceleration.z

        self.p_m = self.imu_data_raw.angular_velocity.x
        self.q_m = self.imu_data_raw.angular_velocity.y
        self.r_m = self.imu_data_raw.angular_velocity.z

    def gps_local_callback(self, msg):
        # print(msg)
        pass

    def gps_rawnav_callback(self, msg):
        self.gps_raw = msg

        self.x_m, self.y_m, self.z_m = transform.geodetic_to_enu(self.gps_raw.latitude, self.gps_raw.longitude, self.gps_raw.altitude, self.lat_ref, self.lon_ref, self.alt_ref)

    def ctrl_callback(self, msg):
        # print(msg.controls)
        ctrl_info_talker(msg.controls[0],msg.controls[1],msg.controls[2],msg.controls[3])
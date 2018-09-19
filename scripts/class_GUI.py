# about QTGUI
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem

class PX4_GUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("gui_TK1.ui", self)
        self.ui.show()

        self.srv_reset = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
        rospy.Subscriber("/iris_cam/image_raw", Image, camera_callback)

        agent1.OT = Offboard_thread(idx_uav=1)

        self.offboard_thread_chk = 2;

        self.slider_roll_1 = self.horizontalSlider_roll_1
        self.slider_pitch_1 = self.verticalSlider_pitch_1
        self.slider_yaw_1 = self.horizontalSlider_yaw_1
        self.slider_throttle_1 = self.verticalSlider_throttle_1

        self.slider_des_x_1 = self.horizontalSlider_des_x_1
        self.slider_des_y_1 = self.horizontalSlider_des_y_1
        self.slider_des_z_1 = self.horizontalSlider_des_z_1

        self.text_des_x_1 = self.plainTextEdit_des_x_1
        self.text_des_y_1 = self.plainTextEdit_des_y_1
        self.text_des_z_1 = self.plainTextEdit_des_z_1

        self.text_state_x_1 = self.plainTextEdit_state_x_1
        self.text_state_y_1 = self.plainTextEdit_state_y_1
        self.text_state_z_1 = self.plainTextEdit_state_z_1

        self.chkbox_FCU_CC = self.checkBox_Conn_FCU_CC
        self.chkbox_CC_GCS = self.checkBox_Conn_CC_GCS

        self.scene = QGraphicsScene()

        self.waypoint_run = 0

        # timer for periodic update of GUI
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)  # Throw event timeout with an interval of 100 milliseconds
        self.timer.timeout.connect(self.update_gui)  # each time timer counts a second, call self.blink
        self.color_flag = True

        self.timer_start()

    def timer_start(self):
        self.timer.start()

    def timer_stop(self):
        self.timer.stop()

    def update_gui(self):
        t = rospy.get_time()

        self.slider_roll_1.setValue(agent1.roll_cmd*100+50)
        self.slider_pitch_1.setValue(agent1.pitch_cmd*100+50)
        self.slider_yaw_1.setValue(agent1.yaw_cmd*100+50)
        self.slider_throttle_1.setValue(agent1.throttle_cmd*100+50)

        self.text_des_x_1.setPlainText(str("{0:.2f}".format(agent1.des_x)))
        self.text_des_y_1.setPlainText(str("{0:.2f}".format(agent1.des_y)))
        self.text_des_z_1.setPlainText(str("{0:.2f}".format(agent1.des_z)))

        self.text_state_x_1.setPlainText(str("{0:.2f}".format(agent1.state.pose.position.x)))
        self.text_state_y_1.setPlainText(str("{0:.2f}".format(agent1.state.pose.position.y)))
        self.text_state_z_1.setPlainText(str("{0:.2f}".format(agent1.state.pose.position.z)))

        if agent1.status.connected == True:
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("connected"))
            self.chkbox_FCU_CC.setCheckState(True)
            self.chkbox_FCU_CC.setText("connected")
        else:
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("disconnected"))
            self.chkbox_FCU_CC.setCheckState(False)
            self.chkbox_FCU_CC.setText("disconnected")

        if agent1.status.armed == True:
            self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("armed"))
        else:
            self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("disarmed"))
        self.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(agent1.status.mode))

        if self.offboard_thread_chk == 1:
            self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("on"))
        elif self.offboard_thread_chk == 2:
            self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("off"))
        elif self.offboard_thread_chk == 3:
            self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("suspend"))
        elif self.offboard_thread_chk == 4:
            self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("on"))

        pixmap = QtGui.QPixmap()
        pixmap.load('catkin_ws/src/wc_gazebo/scripts/camera_image.jpeg')
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    # UAV_1
    @pyqtSlot()
    def slot1(self):  # pushButton_arm
        # self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("armed"))
        agent1.arm(True)

    @pyqtSlot()
    def slot2(self): # pushButton_disarm
        # self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("disarmed"))
        agent1.arm(False)

    @pyqtSlot()
    def slot3(self): # click offboard radio button
        # !! should check there is periodic ctrl command
        check = agent1.mode(custom_mode = "OFFBOARD")
        # if check.success == True:
        #     self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("offboard"))

    @pyqtSlot()
    def slot4(self): # click stabilize radio button
        # check = self.mode(custom_mode="STABILIZED")
        agent1.mode(custom_mode='MANUAL')
        # if check.success == True:
        #     self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("stabilize"))

    @pyqtSlot() ##
    def slot5(self): # click offboard thread on
        if self.offboard_thread_chk == 3:
            agent1.OT.myResume()
            self.offboard_thread_chk = 1
        elif self.offboard_thread_chk == 2:
            agent1.OT.start()
            self.offboard_thread_chk = 1

    @pyqtSlot() ##
    def slot6(self):  # click offboard thread off
        if self.offboard_thread_chk == 1:
            agent1.OT.mySuspend()
            self.offboard_thread_chk = 3
        else:
            agent1.OT.myExit()
            agent1.OT = Offboard_thread(idx_uav=1)
            self.offboard_thread_chk = 2

    @pyqtSlot()
    def slot13(self): # click offboard input as joystick
        self.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem("joystick"))
        self.ctrl_type = 'joystick'

    @pyqtSlot()
    def slot14(self): # click offboard input as autonomous
        self.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem("auto"))
        self.ctrl_type = 'auto'
        print(self.tableWidget.item(2,0).text())
        print(self.tableWidget.item(2,0).text() == 'ff')

    @pyqtSlot()
    def slot15(self): # horizontal slider(desired pos (x))
        agent1.des_x = self.slider_des_x_1.value()

    @pyqtSlot()
    def slot16(self): # horizontal slider(desired pos (y))
        agent1.des_y = self.slider_des_y_1.value()

    @pyqtSlot()
    def slot17(self): # horizontal slider(desired pos (z))
        agent1.des_z = self.slider_des_z_1.value()

    @pyqtSlot()
    def slot18(self): # run waypoint flight (set waypoint trajectory)
        self.traj = traj_gen()
        self.traj.coeff_x = self.traj.calc_coeff(self.traj.wp[0, :], self.traj.T, self.traj.S)
        self.traj.coeff_y = self.traj.calc_coeff(self.traj.wp[1, :], self.traj.T, self.traj.S)
        self.traj.coeff_z = self.traj.calc_coeff(self.traj.wp[2, :], self.traj.T, self.traj.S)
        self.waypoint_run=1

    # reset all
    @pyqtSlot()
    def slot19(self): # reset simulation
        # before reset, set all the desired pos/command to 0
        agent1.des_x = 0
        agent1.des_y = 0
        agent1.des_z = 0
        agent1.roll_cmd = 0
        agent1.pitch_cmd = 0
        agent1.yaw_cmd = 0
        agent1.throttle_cmd = 0.066

        pose = Pose()
        pose.position.x = 0
        pose.position.y = 0
        pose.position.z = 2
        q = quaternion_from_euler(0,0,0)
        pose.orientation = Quaternion(*q)
        state = ModelState()
        state.model_name = "iris"
        state.pose = pose
        self.srv_reset(state)
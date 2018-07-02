import rospy

rospy.init_node('a')
rate = rospy.Rate(20) # 5Hz


while 1:
    print(1)
    rate.sleep()
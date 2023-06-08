#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import re
import time


class ControlNode(object):
    def __init__(self):
        rospy.init_node('control_node', anonymous=True)
        self.subscriber = rospy.Subscriber(
            'chatgpt_node', String, self.listener_callback, queue_size=10)
        self.publisher_ = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.history = ""

    def listener_callback(self, msg):
        # 处理接收到的消息。
        print("start parse msg")
        strlx = re.compile(r"linear.x = (.*?)(?![\d.-])")
        strly = re.compile(r"linear.y = (.*?)(?![\d.-])")
        strlz = re.compile(r"linear.z = (.*?)(?![\d.-])")
        strax = re.compile(r"angular.x = (.*?)(?![\d.-])")
        stray = re.compile(r"angular.y = (.*?)(?![\d.-])")
        straz = re.compile(r"angular.z = (.*?)(?![\d.-])")
        input_text = msg.data
        twist = Twist()
        if re.search(strlx, input_text):
            val_linear_x = re.search(strlx, input_text).group(1)
            twist.linear.x = float(val_linear_x)
            print(val_linear_x, end=" ")
        if re.search(strly, input_text):
            val_linear_y = re.search(strly, input_text).group(1)
            twist.linear.y = float(val_linear_y)
            print(val_linear_y, end=" ")
        if re.search(strlz, input_text):
            val_linear_z = re.search(strlz, input_text).group(1)
            twist.linear.z = float(val_linear_z)
            print(val_linear_z, end=" ")
        if re.search(strax, input_text):
            val_angular_x = re.search(strax, input_text).group(1)
            twist.angular.x = float(val_angular_x)
            print(val_angular_x, end=" ")
        if re.search(stray, input_text):
            val_angular_y = re.search(stray, input_text).group(1)
            twist.angular.y = float(val_angular_y)
            print(val_angular_y, end=" ")
        if re.search(straz, input_text):
            val_angular_z = re.search(straz, input_text).group(1)
            twist.angular.z = float(val_angular_z)
            print(val_angular_z)

        self.publisher_.publish(twist)
        time.sleep(1.5)
        twist0 = Twist()
        self.publisher_.publish(twist0)

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        node = ControlNode()
        node.run()
    except rospy.ROSInterruptException:
        pass


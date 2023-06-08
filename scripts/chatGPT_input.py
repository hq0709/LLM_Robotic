#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from chatgpt_test.msg import MarkResult

class PublisherNode(object):
    def __init__(self):
        rospy.init_node('publisher_node', anonymous=True)
        self.sub = rospy.Subscriber("/uSingleArucoMark/marker", MarkResult, self.callback, queue_size=10)
        self.pub = rospy.Publisher('user_input', String, queue_size=10)
        self.user_input_enabled = False
        self.flag_received = False
        self.latest_msg = None

    def callback(self, data):
        if self.user_input_enabled or self.flag_received:
            return

        if data.flag:
            self.flag_received = True
            self.latest_msg = data

    def process_marker_message(self):
        if self.latest_msg is not None:
            msg = String()
            result_str = "({}, {}, {}, {})".format(self.latest_msg.flag, self.latest_msg.direction, self.latest_msg.distance, self.latest_msg.angle)
            rospy.loginfo("Received MarkResult message: %s", result_str)
            msg.data = result_str
            self.pub.publish(msg)
            self.latest_msg = None

    def process_user_input(self):
        user_input = input("Enter user input (press Enter twice to finish):\n")
        user_input_lines = []
        while user_input.strip() != "":
            user_input_lines.append(user_input)
            user_input = input()
        user_msg = "\n".join(user_input_lines)
        msg = String()
        msg.data = user_msg
        self.pub.publish(msg)

    def run(self):
        while not rospy.is_shutdown():
            user_input = input("Please input ('m' to receive marker, 'u' to enable user input): ")
            if user_input == 'm':
                self.flag_received = False
                self.user_input_enabled = False
                self.process_marker_message()
            elif user_input == 'u':
                self.flag_received = False
                self.user_input_enabled = True
                self.process_user_input()
            else:
                rospy.logwarn("Invalid input. Please try again.")

if __name__ == '__main__':
    try:
        node = PublisherNode()
        node.run()
    except rospy.ROSInterruptException:
        pass


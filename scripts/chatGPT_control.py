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
        self.history = []

    def parse_command(self, command):
        twist = Twist()
        time_value = None

        # 使用正则表达式提取指定格式的内容
        twist_str = re.search(r"linear\.x\s*=\s*([\d.-]+),\s*linear\.y\s*=\s*([\d.-]+),\s*linear\.z\s*=\s*([\d.-]+),\s*angular\.x\s*=\s*([\d.-]+),\s*angular\.y\s*=\s*([\d.-]+),\s*angular\.z\s*=\s*([\d.-]+),\s*time\s*=\s*([\d.-]+)", command)
        if twist_str:
            twist.linear.x = float(twist_str.group(1))
            twist.linear.y = float(twist_str.group(2))
            twist.linear.z = float(twist_str.group(3))
            twist.angular.x = float(twist_str.group(4))
            twist.angular.y = float(twist_str.group(5))
            twist.angular.z = float(twist_str.group(6))
            time_value = float(twist_str.group(7))

        return twist, time_value

    def listener_callback(self, msg):
        input_text = msg.data
        commands = input_text.split('\n')

        for command in commands:
            twist, time_value = self.parse_command(command)
            if twist is not None and time_value is not None:
                start_time = rospy.Time.now()
                end_time = start_time + rospy.Duration(time_value)

                rate = rospy.Rate(10)  # 发布频率为10Hz

                while rospy.Time.now() < end_time:
                    self.publisher_.publish(twist)
                    rate.sleep()

                # 发布空的 Twist 来停止小车移动
                stop_twist = Twist()
                self.publisher_.publish(stop_twist)

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        node = ControlNode()
        node.run()
    except rospy.ROSInterruptException:
        pass


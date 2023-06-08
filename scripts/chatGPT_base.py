#!/usr/bin/env python

import os
import rospy
from std_msgs.msg import String
import openai

##from revChatGPT.V1 import Chatbot
import re



openai.api_key = "your_api_key"

class OpenAINode(object):
    def __init__(self):
        rospy.init_node('openai_node', anonymous=True)
        self.generate_code = rospy.get_param('~generate_code', True)
        self.revChatGPT = rospy.get_param('~revChatGPT', False)
        self.publisher_ = rospy.Publisher('chatgpt_node', String, queue_size=10)
        self.subscription = rospy.Subscriber(
            'user_input',
            String,
            self.listener_callback,
            queue_size=10)
        self.history = ""
        rospy.loginfo("init success")

    def listener_callback(self, msg):
        
        input_text = msg.data
        pub_msg = String()
        rospy.loginfo("start get respones") 
        if self.revChatGPT == False:
            self.history += input_text 
            self.history += " "
      
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": self.history+input_text}
                ]
            )
            pub_msg.data = response['choices'][0]['message']['content']
            
            print(pub_msg.data)
            self.history += pub_msg.data
            self.history += " "
        else:
            prev_text = ""
            for data in chatbot.ask(input_text,):
                message = data["message"][len(prev_text):]
                print(message,end="",flush=True)

                prev_text = data["message"]
            pub_msg.data = prev_text
        #if self.generate_code == True:
         #   start = "```python"
         #   end = "```"
         #   if start in prev_text and end in prev_text:
         #       start_index = prev_text.index(start) + len(start)
         #       end_index = prev_text.index(end, start_index)
         #       result = prev_text[start_index:end_index].strip()
         #       self.file = open(os.getcwd()+'/src/chatGPT_test/chatGPT_test/chatGPT_code.py', 'w')
         #       self.file.write(result)
         #       self.file.close()
         #       os.system("bash build_run.sh")
        print()
        self.publisher_.publish(pub_msg)

def main():
    chatgpt_node = OpenAINode()
    rospy.spin()

if __name__ == '__main__':
    main()


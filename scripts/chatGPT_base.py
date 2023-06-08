#!/usr/bin/env python

import os
import rospy
from std_msgs.msg import String
import openai

##from revChatGPT.V1 import Chatbot
import re


#chatbot = Chatbot(config={
 #   "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ3YW5neWkuY3h5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLVJKd3d0amg1YUt1bUtkR1Y1QUNxeExoZiJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI4ODQyMDI0Mzg2MzM5MjU0NDUiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjg0MjE3NjU2LCJleHAiOjE2ODU0MjcyNTYsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIn0.a6JS34qFItuaC7nrJePxxenj8FNlI0RM1f8p9uSGMWAtY-1fWvgEv5jKYxZLTvwZpwyG85fyhV9TaCVQ2NpIuaSeMxW2ZFyBmE2ZDZOZ0AcabmY6DC4XKAmTvSb7c7xYe4UMceLY_GOWNB9kET9n81ienQOfKfHe-b7QSXHhykXXm1SBdFS5W8-AyKMtJq4biwZg09N3kSrvZlYxyDW1Uv0mmKenL6lCribONTvXl78n8pzURmNLoKDKgMRrsWXa2Du9bQqf207jX5t9ZDwIV4eWL8EreCU8BbqGx6hnVhbvOAR9GD5eLqv5pzvPCXBY6GruUsSxvMW_hkRizsGTwA"
#})
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


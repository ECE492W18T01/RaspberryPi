''' Drive

Main program used for driving the crawler using the dualshock 4 controller.

TODO:
- Implement a queue/messaging system for the threads to exchange data.
- Set variables using configuration file.
- Implement threading classes in seperate module (optional).
'''

import io
import socket
import struct
from time import sleep
import requests
import sys
import threading
from modules.controller import DS4
from modules.crawler import Crawler


#URL = "http://crawler.us-west-2.elasticbeanstalk.com/api/update/"
URL = "http://192.168.0.4:8080/api/update/"
API_UPDATE = URL + "/api/update/"
INSTRUCTION_POLL_FREQUENCY = 10
SERVER_UPDATE_FREQUENCY = 1


crawler = Crawler()

class updateAPI(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency

    def run(self):
        while True:
            try:
                r = requests.post(URL, data={'crawler': crawler.info() })
                sleep(1/self.frequency)
            except:
                print("Failed to POST to ", URL)
                sleep(10)


class Drive(threading.Thread):
    
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.controller = DS4()
        self.throttle_input = self.controller.RIGHT_Y_AXIS
        self.steering_input = self.controller.LEFT_X_AXIS
        self.brake_input = self.controller.L2
        self.end = self.controller.SHARE

    def run(self):
        while True:
            self.controller.connect()
            while self.controller.is_connected():
                crawler.connect()
                while crawler.is_connected():
                    self.get_instructions()
                    crawler.send_instructions()
                    ''' Recieving instructions
                    crawler.recieve_instruction()
                    if crawler.recieved == crawler.comm.end:
                        crawler.connect = 0
                    '''
                    sleep(1/crawler.comm['instruction_freq'])
                sleep(1/crawler.comm['connect_freq'])
        

    def get_instructions(self):
            enabled = self.controller.get_button(self.controller.R2)
            crawler.set_motor_instruction(self.controller.get_axes()[self.throttle_input])
            crawler.set_steering_instruction(self.controller.get_axes()[self.steering_input])
            crawler.set_brake_instruction(self.controller.get_button(self.brake_input))
            '''
            end = self.controller.get_button(self.end)
            print(end)
            if end == 1:
                crawler.disconnect()
            '''




crawler_thread = Drive('Crawler Thread')
network_thread = updateAPI('Network Thread', SERVER_UPDATE_FREQUENCY)

crawler_thread.start()
network_thread.start()

crawler_thread.join()
network_thread.join()

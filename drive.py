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
import time
import requests
import sys
import threading
from modules.controller import DS4
from modules.crawler import Crawler

#AWS_URL = "http://crawler.us-west-2.elasticbeanstalk.com/api/update/"
LOCAL_URL = "http://192.168.0.4:8080/api/update/"
API_UPDATE = SERVER_URL + "/api/update/"
INSTRUCTION_POLL_FREQUENCY = 10
SERVER_UPDATE_FREQUENCY = 1

controller = DS4()
controller.connect()

crawler = Crawler()

class updateAPI(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency

    def run(self):
        while True:
            r = requests.post(LOCAL_URL, data={'crawler': crawler.info() })
            time.sleep(1/self.frequency)


class Drive(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency

    def run(self):
        while True:
            crawler.connect()
            while crawler.connected == 1:
                self.get_instructions()
                crawler.send_instruction()
                ''' Recieving instructions
                crawler.recieve_instruction()
                if crawler.recieved == crawler.comm.end:
                    crawler.connect = 0
                '''
                sleep(1/crawler.comm.instruction_freq)
            sleep(1/crawler.comm.connect_freq)

    def get_instructions():
            enabled = controller.get_button(controller.R2)
            if enabled == 1:
                crawler.set_motor_instruction(controller.get_axis()[controller.RIGHT_Y_AXIS])
                crawler.set_steering_instruction(controller.get_axis()[controller.LEFT_X_AXIS])
                print("Crawler info: %o" ,crawler.info())



crawler_thread = Drive('Crawler Thread', INSTRUCTION_POLL_FREQUENCY)
network_thread = updateAPI('Network Thread', SERVER_UPDATE_FREQUENCY)

crawler_thread.start()
network_thread.start()

crawler_thread.join()
network_thread.join()

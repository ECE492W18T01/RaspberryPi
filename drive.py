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
                sleep(1/self.frequency * 10)


class Drive(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency
        self.controller = DS4()

    def run(self):
        while True:
            self.controller.connect()
            while self.controller.is_connected():
                crawler.connect()
                while crawler.is_connected():
                    self.get_instructions()
                    crawler.send_instruction()
                    ''' Recieving instructions
                    crawler.recieve_instruction()
                    if crawler.recieved == crawler.comm.end:
                        crawler.connect = 0
                    '''
                    sleep(1/crawler.comm['instruction_freq'])
                sleep(1/crawler.comm['connect_freq'])
        

    def get_instructions():
            enabled = self.controller.get_button(controller.R2)
            if enabled == 1:
                crawler.set_motor_instruction(self.controller.get_axes()[self.controller.RIGHT_Y_AXIS])
                crawler.set_steering_instruction(self.controller.get_axes()[self.controller.LEFT_X_AXIS])
                print("Crawler info: %o" ,crawler.info())



crawler_thread = Drive('Crawler Thread', INSTRUCTION_POLL_FREQUENCY)
network_thread = updateAPI('Network Thread', SERVER_UPDATE_FREQUENCY)

crawler_thread.start()
network_thread.start()

crawler_thread.join()
network_thread.join()

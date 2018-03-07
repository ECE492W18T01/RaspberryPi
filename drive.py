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

SERVER_URL = "http://192.168.0.4:8080/api/update/"
API_UPDATE = SERVER_URL + "/api/update/"
INSTRUCTION_POLL_FREQUENCY = 10
SERVER_UPDATE_FREQUENCY = 1

controller = DS4()
controller.connect()

crawler = Crawler()
crawler.connect()

class updateAPI(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency

    def run(self):
        while True:
            r = requests.post(SERVER_URL, data={'crawler': crawler.info() })
            time.sleep(1/self.frequency)

class getInstructions(threading.Thread):
    def __init__(self, name, frequency):
        threading.Thread.__init__(self)
        self.name = name
        self.frequency = frequency

    def run(self):
        while True:
            crawler.set_motor(controller.get_button(controller.R2))
            crawler.set_steering(controller.get_axis()[controller.LEFT_X_AXIS])
<<<<<<< HEAD
            #crawler.send_instructions()
            print("Crawler info: %o" ,crawler.info())
=======
            crawler.send_instructions()
>>>>>>> 2fffcd999ee4fd479749b80e76329711db53cb90
            time.sleep(1/self.frequency)

instruction_thread = getInstructions('Instruction Thread', INSTRUCTION_POLL_FREQUENCY)
network_thread = updateAPI('Network Thread', SERVER_UPDATE_FREQUENCY)


instruction_thread.start()
network_thread.start()

instruction_thread.join()
network_thread.join()

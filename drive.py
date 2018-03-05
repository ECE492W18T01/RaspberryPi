import io
import socket
import struct
import time
import requests
import sys

from modules.controller import DS4
from modules.crawler import Crawler

SERVER_URL = "http://192.168.0.4:8080"
API_UPDATE = SERVER_URL + "/api/update/"


controller = DS4()
controller.connect()

crawler = Crawler()
#crawler.connect()

try:
    while True:
        crawler.set_motor(controller.get_button(controller.R2))
        crawler.set_steering(controller.get_axis()[controller.LEFT_X_AXIS])
        #crawler.send_instructions()

        print(crawler)
        r = requests.post(API_UPDATE, data={'crawler': 'crawler data here'})
        print(r.text)
        sleep(0.1)
finally:
    controller.disconnect()
    crawler.disconnect()

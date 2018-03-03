import io
import socket
import struct
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
#import cv2
from modules.controller import DS4
from modules.crawler import Crawler
from modules.network import Network

def get_instructions(controller):
    motor = controller.get_button(controller.R2)
    steering = controller.get_axes()[controller.LEFT_X_AXIS]
    return (motor, steering)

'''
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
time.sleep(0.1)
'''

controller = DS4()
controller.connect()

crawler = Crawler()
#crawler.connect()

network = Network()
network.connect()

try:
    while True:
        data = 1
        #network.send(data)

        crawler.set_motor(controller.get_button(controller.R2))
        crawler.set_steering(controller.get_axes()[controller.LEFT_X_AXIS])
        #crawler.send_instructions()
        
        
finally:
    network.finish()
    controller.disconnect()

import io
import socket
import struct
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from modules.controller import DS4
from modules.crawler import Crawler
from modules.network import Network


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
time.sleep(0.1)

controller = DS4()
controller.connect()

crawler = Crawler()
#crawler.connect()

network = Network(enable=False)
network.connect()

try:
    while True:
        data = 1
        network.send(data)

        crawler.set_motor(controller.get_button(controller.R2))
        crawler.set_steering(controller.get_axis()[controller.LEFT_X_AXIS])
        crawler.send_instructions()
        sleep(0.1)
finally:
    network.finish()
    controller.disconnect()
    crawler.disconnect()

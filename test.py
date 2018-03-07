'''
'''

from picamera import PiCamera
from time import sleep
from modules.controller import DS4
from modules.crawler import Crawler
import serial
import requests

def crawler_test():
    crawler = Crawler()
    try:
        crawler.connect()
        crawler.set_motor(1)
        crawler.set_steering(1)
        crawler.send_instructions()
    finally:
        crawler.disconnect()


def controller_test():
    print("Controller test started..")
    controller = DS4()
    controller.connect()
    print(controller.name)
    testing = True
    try:
        while testing:
            print("R2: ", controller.get_button(controller.R2))
            print("X: ", controller.get_axis()[controller.LEFT_X_AXIS], "\n")
            sleep(0.2)

    except KeyboardInterrupt:
        testing = False

    finally:
        controller.disconnect()
        print("Controller test ended.")


def camera_preview():
    print("Camera preview Started, please have monitor connected..")
    camera = PiCamera()
    camera.start_preview()
    sleep(10)
    camera.stop_preview()
    print("Camera preview has ended.")


def serial_test():
    port = serial.Serial("/dev/serial0", baudrate=115200, timeout=3.0)
    try:
        while True:
            port.write("Testing...")
            time.sleep(1)
            recieved = port.read(10)
            print("Recieved")
    finally:
        print("Completed serial test.")

def request_test():
    UPDATE_URL = "http://192.168.0.4:8080/api/update/"
    r = requests.post(UPDATE_URL, data={'crawler': 'crawler data here'})

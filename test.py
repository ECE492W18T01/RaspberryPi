#from picamera import PiCamera
from time import sleep
from modules.controller import DS4
from modules.crawler import Crawler
import RPi.GPIO as GPIO
import serial


def gpio_test():
    output_pin = 24
    ON = 1
    OFF = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(output_pin, GPIO.OUT)

    try:
        while True:
            GPIO.output(output_pin, ON)
            sleep(0.5)
            GPIO.output(output_pin, OFF)
            sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()


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
    camera = PiCamera()
    camera.start_preview()
    sleep(10)
    camera.stop_preview()


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

controller_test()

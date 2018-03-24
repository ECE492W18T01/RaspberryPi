''' Test
Crawler and peripheral testing.

TODO:
- Finish writing test cases.
- Automate testing using unit testing modules (optional).
- Implement logging system to log all testing information (optional).
'''

#from picamera import PiCamera
from time import sleep
from modules.controller import DS4
from modules.messaging import OutboundMessaging, InboundMessaging
from crawler import Crawler
import serial
import requests
import configparser
import logging

def outbound_test():
    port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=3.0)
    port.write('*'.encode())
    port.write("Hello".encode())
    '''
    message = ""
    outbound_thread = OutboundMessaging(port, 0.1, message)
    print(outbound_thread.message)
    for i in range(30):
        outbound_thread.set_message(str(i))
        outbound_thread.send_message()
        sleep(1)
        '''

outbound_test()

def inbound_test():
    port = serial.Serial('dev/ttyUSB0', baudrate=115200, timeout=3.0)
    message = ""
    inbound_thread = InboundMessaging(port, 0.1, message)
    inbound_thread.start()
    for i in range(30):
        outbound_thread.get_message()
        delay(1)
        
#inbound_test()

def crawler_test():
    #Attempts to connect with the crawler and send instructions. 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('Crawler Test')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('logs/drive.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    config = configparser.ConfigParser()
    config.read('config.ini')
    crawler = Crawler(logger, config['COMMUNICATION'])
    controller = DS4()
    try:
        controller.connect()
        #controller.start()
        #controller.join()
        crawler.connect()
        while True:
            print('.')
            controller.get_buttons()
            controller.get_axes()
            crawler.set_motor_instruction(controller.axes[controller.RIGHT_Y_AXIS])
            crawler.set_steering_instruction(controller.axes[controller.LEFT_X_AXIS])
            crawler.set_brake_instruction(controller.buttons[controller.L2])
            crawler.set_instruction_message()
            print(crawler.instructions)
            sleep(0.2)
    finally:
        print('Crawler Test Done.')
        crawler.disconnect()
        controller.disconnect()

#crawler_test()


def controller_test():
    ''' Polls connected bluetooth controller for some amount of time '''
    print("Controller test started..")
    controller = DS4()
    controller.run()
    '''
    controller.connect()
    print(controller.name)
    print(controller.connected)
    try:
        while controller.is_connected():
            print("R2: ", controller.get_button(controller.R2))
            print("X: ", controller.get_axes()[controller.LEFT_X_AXIS])
            print(controller.connected)
            sleep(0.5)

    except KeyboardInterrupt:
        controller.connected = False

    finally:
        controller.disconnect()
        print("Controller test ended.")
        '''

#controller_test()



def camera_preview():
    ''' Quick picamera preview '''
    print("Camera preview Started, please have monitor connected..")
    camera = PiCamera()
    camera.start_preview()
    sleep(10)
    camera.stop_preview()
    print("Camera preview has ended.")

#camera_preview()


def serial_test():
    ''' Serial test used to ensure proper setup between de10 and RPI '''
    device = '/dev/ttyUSB0'
    port = serial.Serial(device, baudrate=115200, timeout=3.0)
    try:
        while True:
            port.write('*'.encode())
            sleep(1)

    except KeyboardInterrupt:
        print("Ending session.")

    finally:
        port.close()
        print("Completed serial test.")

#serial_test()

def request_test():
    ''' API update test '''
    UPDATE_URL = "http://192.168.0.4:8080/api/update/"
    r = requests.post(UPDATE_URL, data={'crawler': 'crawler data here'})

#request_test()

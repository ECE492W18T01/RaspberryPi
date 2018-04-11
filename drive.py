''' Drive

Main program used for driving the crawler using the dualshock 4 controller.

TODO:
- Implement a queue/messaging system for the threads to exchange data.
- Set variables using configuration file.
- Implement threading classes in seperate module (optional).
'''

import logging
import configparser
import io
import socket
import struct
from time import sleep
import requests
import sys
import threading

from modules.controller import DS4
from modules.network import Network

from crawler import Crawler


class Drive(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.initialize_logger()
        self.logger.info('Starting drive service.')
        self.crawler = Crawler(self.logger, self.config['COMMUNICATION'])
        self.controller = DS4()
        self.initialize_inputs()


    def initialize_inputs(self):
        ''' Map controller inputs to Crawler inputs. '''
        self.throttle_input = self.controller.RIGHT_Y_AXIS
        self.steering_input = self.controller.LEFT_X_AXIS
        self.brake_input = self.controller.L2
        self.end_input = self.controller.SHARE

    def run(self):
        '''
            Run the drive process.
         '''
        print('Running..')

        try:
            while True:
                if self.controller.connect():
                    self.logger.debug('Controller connected.')
                    print('Controller connected')
                while self.controller.is_connected():
                    self.crawler.connect()
                    while self.crawler.is_connected():
                        #print('.')
                        self.set_instructions()
                        self.crawler.set_instruction_message()
                        self.crawler.send_message()
                        self.crawler.recieve_messages()
                        sleep(1/self.controller.POLL_FREQUENCY)
                    sleep(1/self.controller.CONNECT_FREQUENCY)
                self.logger.warning('No controller connected.')
        except KeyboardInterrupt:
            print('Shutting down')
            self.logger.info('Shutting down.')
        finally:
            self.controller.disconnect()
            self.crawler.disconnect()
            return

    def set_instructions(self):
        ''' Get instructions from the controller and send them to the Crawler. '''
        self.controller.get_buttons()
        self.controller.get_axes()
        self.crawler.set_motor_instruction(self.controller.axes[self.throttle_input])
        self.crawler.set_steering_instruction(self.controller.axes[self.steering_input])

    def initialize_logger(self):
        ''' Initialize the logger handlers for the drive class. '''
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.config['LOGGING']['Name'])
        self.logger.setLevel(self.config['LOGGING']['Level'])
        self.initialize_logger_handler(self.config['LOGGING']['DebugFile'], format)


    def initialize_logger_handler(self, file, format):
        fh = logging.FileHandler(self.config['LOGGING']['Directory'] + '/' + file)
        fh.setFormatter(format)
        self.logger.addHandler(fh)

drive = Drive()
drive.run()

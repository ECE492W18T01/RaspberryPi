''' Messaging
Serial messaging interface used to send and recieve messages from the serial port. 
'''
import threading
from threading import Condition
import serial
import time
from time import sleep
import re
import json
from queue import Queue


class InboundMessaging(threading.Thread):
    read_size = 128
    frequency = 10

    def __init__(self, port, pattern, queue):
        threading.Thread.__init__(self)
        self.port = port
        self.pattern = pattern
        self.queue = queue

    def run(self):
        ''' Read messages from the serial port and sleep when not reading. '''
        while True:
            try:
                print('Recieving messages.')
                buffer = self.port.read(self.read_size)
                self.decode_messages(buffer)
            except:
                print('Port busy.')
            finally:
                sleep(1/self.frequency)

    def decode_messages(self, buffer):
        ''' Decode messages from the read buffer. '''
        matches = self.pattern.findall(buffer.decode())
        for match in matches:
            message = re.sub('\n', '', re.sub('!', '', match))
            self.queue.put(message)


class SerialMessaging():
    symbols = {
        'connect': '*',
        'disonnect': '&',
        'ack': '@',
        'start': '!',
        'end': '\r'
    }

    read_size = 256
    is_connected = False
    outbound_service_set = False
    inbound_service_set = False
    buffer = None
    port = None

    def __init__(self, options, inbound_queue):
        self.options = options
        self.configure(options)
        self.inbound_messages = inbound_queue
        self.pattern = re.compile('!.*\n')
        self.threads = []

    def connect(self):
        ''' Attempt to create serial port for communication. '''
        self.port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=0.5)
        self.is_connected = True
        return self.is_connected

    def authorize(self):
        ''' Authorize communication with Crawler. '''
        print('Initializing communication.')
        print(self.symbols['connect'])
        self.port.write(str(self.symbols['connect']).encode())
        return True

    def disconnect(self):
        self.is_connected = False
        return True

    def set_message(self, message):
        ''' Set ouobound message for the serial port. '''
        self.outbound_message = message

    def send_message(self):
        ''' Send the current outbound message to the connected serial port. '''
        self.port.write(self.outbound_message.encode())
        return True

    def recieve_messages(self):
        ''' Recieve messages on seperate thread to avoid blocking. '''
        inbound_service = InboundMessaging(self.port, self.pattern, self.inbound_messages)
        inbound_service.start()
        

    def decode_messages(self, buffer):
        ''' Decode method used to getting messages from a read buffer. '''
        matches = self.pattern.findall(buffer.decode())
        for match in matches:
            message = re.sub('\n', '', re.sub('!', '', match))
            self.outbound_messages.put(message)


    def set_outbound_message(self, message):
        self.outbound_message = message
        return True

    def get_inbound_message(self, message):
        return self.inbound_message

    def configure(self, options):
        self.baudrate = int(options['Baudrate'])
        self.timeout = float(options['Timeout'])
        self.device = options['Device']
        return True

import threading
from threading import Condition
import serial
import time
from time import sleep
import re
import json
from queue import Queue

class OutboundMessaging(threading.Thread):
    message = ""

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        self.port.write(self.message)

    def set_message(self, message):
        self.message = message.encode()
        return True


class InboundMessaging(threading.Thread):
    read_size = 128
    status = False

    def __init__(self, port, pattern, queue):
        threading.Thread.__init__(self)
        self.port = port
        self.pattern = pattern
        self.queue = queue

    def run(self):
        buffer = self.port.read(self.read_size)
        self.decode_messages(buffer)

    def decode_messages(self, buffer):
        matches = self.pattern.findall(buffer.decode())
        for match in matches:
            message = re.sub('\n', '', re.sub('!', '', match))
            self.outbound_messages.put(message)

    def get_message(self):
        return this.message

    def get_status(self):
        return this.status


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
    outbound_messages = None
    outbound_service_set = False
    inbound_message = ""
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
        self.outbound_message = message

    def send_message(self):
        #flush before writing
        self.outbound_service = OutboundMessaging(self.port, 0.1)
        self.outbound_service.set_message(self.outbound_message.encode())
        self.outbound_service.start()
        #self.port.write(self.outbound_message.encode())
        #self.outbound_service.start()
        return True

    def recieve_messages(self):
        self.inbound_service = InboundMessaging(self.port, 0.2, )
        self.inbound_service.start()
        #self.decode_messages(self.port.read(self.read_size))
        #flush after reading
        return self.inbound_message

    def decode_messages(self, buffer):
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

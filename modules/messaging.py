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
    status = False

    def __init__(self, port, frequency):
        threading.Thread.__init__(self)
        self.port = port
        self.frequency = frequency

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                self.port.write(self.message)
                self.status = True
            except:
                print("Outbound messaging stopped working.")
                self.status = False
            sleep(1/self.frequency)

    def end(self):
        self.is_running = False

    def send_messsage(self):
        self.port.write(this.message.encode())
        return True

    def set_message(self, message):
        self.message = message.encode()
        return True

    def get_status(self):
        return self.status


class InboundMessaging(threading.Thread):
    read_size = 128
    message = ""
    status = False

    def __init__(self, port, frequency):
        threading.Thread.__init__(self)
        self.port = port
        self.frequency = frequency

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                self.message = self.port.read(self.read_size)
                self.status = True
            except:
                print("Inbound message not recieved.")
                self.status = False
            sleep(1/self.frequency)

    def end(self):
        self.is_running = False

    def read_message(self):
        self.message = self.port.read(self.read_size)
        return self.message

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

    def __init__(self, options, outbound_queue):
        self.options = options
        self.configure(options)
        self.outbound_service = OutboundMessaging(self.port, 0.1)
        self.inbound_service = InboundMessaging(self.port, 0.2)
        self.outbound_messages = outbound_queue
        self.pattern = re.compile('!.*\n')
        self.threads = []

    def connect(self):
        ''' Attempt to create serial port for communication. '''
        self.port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=3.0)
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

    def start_services(self):
        print('Starting messaging services.')
        self.outbound_service.start()
        self.outbound_service_set = True
        self.inbound_service.start()
        self.inbound_service_set = True

    def end_services(self):
        print('Ending messaging services.')
        self.outbound_service_set = False
        self.outbound_service.end()
        self.inbound_service_set = False
        self.inbound_service.end()
        
    def set_message(self, message):
        self.outbound_message = message

    def send_message(self):
        #flush before writing
        self.port.write(self.outbound_message.encode())
        #self.outbound_service.start()
        return True

    def recieve_messages(self):
        self.decode_messages(self.port.read(self.read_size))
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


class SerialPort():
    port = None
    device = '/dev/ttyUSB0'

    def __init__(self):
        condition = Condition()

    def connect(self):
        print('Creating port..')
        self.port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=3.0)
        return True

    def write(self, message):
        with self.condition:
            self.port.write()
            self.condition.notify_all()
        return True

    def read(self):
        with self.condition:
            message = self.port.read()
            self.condition.notify_all()
        return message

import threading
from threading import Condition
import serial
import time
from time import sleep

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

    def __init__(self, port, frequency, message):
        threading.Thread.__init__(self)
        self.port = port
        self.frequency = frequency
        self.message = message

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
    outbound_message = ""
    outbound_service_set = False
    inbound_message = ""
    inbound_service_set = False
    buffer = None

    def __init__(self, options):
        self.options = options
        self.configure(options)
        self.port = SerialPort()
        self.outbound_service = OutboundMessaging(self.port, 0.1, self.outbound_message)
        self.inbound_service = InboundMessaging(self.port, 0.2, self.inbound_message)
        self.threads = []

    def connect(self):
        ''' Attempt to create serial port for communication. '''
        self.is_connected = self.port.connect()
        return self.is_connected

    def authorize(self):
        ''' Authorize communication with Crawler. '''
        print('Initializing communication.')
        print(self.symbols['connect'])
        self.port.write(str(self.symbol['connect']).encode())
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

    def send_message(self):
        self.port.write(self.outbound_outbound.encode())
        #self.outbound_service.start()
        return True

    def recieve_message(self):
        recieve_buffer = self.port.read(256)
        time = time.time()
        if recieve_buffer[0] is self.symbols.start:
            #Read up to end character
            #Convert to JSON object
            #Identify message type
            #Return message
        return (message, time)

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

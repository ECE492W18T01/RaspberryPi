import threading
import serial
from time import sleep

class OutboundMessaging(threading.Thread):
    message = ""
    status = False

    def __init__(self, port, frequency, message):
        threading.Thread.__init__(self)
        self.port = port
        self.frequency = frequency
        self.message = message
        

    def run(self):
        while True:
            try:
                self.port.write(self.message)
                status = True
            except:
                print("Outbound messaging stopped working.")
                status = False
            sleep(1/self.frequency)
        

    
    def send_messsage(self):
        print('hello')
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
        while True:
            try:
                self.message = self.port.read(self.read_size)
                self.status = True
            except:
                print("Inbound message not recieved.")
                self.status = False
            sleep(1/self.frequency)
    
    def read_message(self):
        message = self.port.read(self.read_size)
        return message

    def get_message(self):
        return this.message
    
    def get_status(self):
        return this.status
    
class SerialMessaging():
    symbol = {
        'connect': '*',
        'disonnect': '&',
        'ack': '@'
    }
    port = None
    read_size = 256
    is_connected = False
    
    def __init__(self, options, outbound, inbound):
        self.options = options
        self.configure(options)
        self.outbound = outbound
        self.inbound = inbound
        
    def connect(self):
        ''' Attempt to create serial port for communication. '''
        self.port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=3.0)
        #self.outbound = OutboundMessaging(self.port, 0.1, "")
        #self.inbound = InboundMessaging(self.port, 0.2, "")
        self.is_connected = True
        return True
        
    def authorize(self):
        ''' Authorize communication with Crawler. '''
        print('Initializing communication.')
        print(self.symbol['connect'])
        self.port.write(str(self.symbol['connect']).encode())
        #self.port.write('*')
        sleep(0.5)
        msg = self.port.read(self.read_size).decode()
        print(msg)
        '''
        if msg == self.acknowledgment:
            return True
        else:
            return False
        '''
        return True
        
    
    def disconnect(self):
        #if self.port is not None:
            #self.port.write(self.disconnect.encode())
            #self.port.disconnect()
        return True
    
    def start_communication(self):
        print('Starting communication.')
        #self.outbound.start()
        #self.outbound.join()
        #self.inbound.start()
        
    def send_message(self):
        self.port.write(self.outbound.encode())
        return True
        
    def set_message(self, message):
        print('set message')
        self.outbound = message
        return True
        
    def configure(self, options):
        self.baudrate = int(options['Baudrate'])
        self.timeout = float(options['Timeout'])
        self.device = options['Device']
        return True
    
    def test(self):
        print('Testing')
        return True
        
    
    

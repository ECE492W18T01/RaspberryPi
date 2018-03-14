''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''

import serial

class Crawler:
    ON = 1
    OFF = 0
    CENTER = 0.0
    BAUDRATE = 115200
    TIMEOUT = 3.0
    READ_SIZE = 10
    DEVICE = '/dev/ttyUSB0'

    port = None

    motor = 0
    steering = CENTER

    wheels = {
        'fl' : 0,
        'fr' : 0,
        'rl' : 0,
        'rr' : 0
    }

    battery = 0

    def info(self):
        ''' Return dictionary of Crawler status. '''
        return {
            'baudrate' : self.BAUDRATE,
            'motor' : self.motor,
            'wheels' : self.wheels
            }

    def connect(self):
        ''' Establish serial connection with Crawler(DE10). '''
        self.port = serial.Serial(self.DEVICE, baudrate=self.BAUDRATE, timeout=self.TIMEOUT)
        self.port.write('Connect request\r'.encode())
        print('Crawler connected on serial0')

    def set_motor(self, mode):
        ''' Set the desired mode for the crawler motor. '''
        self.motor = mode


    def set_steering(self, input):
        ''' Set desired steering instruction. '''
        self.steering = input * 60


    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        instructions = str(self.motor) + ',' + str(self.steering) + '\r'
        self.port.write(instructions.encode())
        #recieved = self.port.read(READ_SIZE)

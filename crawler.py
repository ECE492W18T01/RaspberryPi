''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import serial
from time import sleep
from modules.messaging import SerialMessaging
from math import pow

class Crawler():
    ON = 1
    OFF = 0
    CENTER = 0.0

    connected = False

    status = {
        'mode' : 0,
        'motors' : CENTER,
        'steering' : CENTER,
        'battery' : 0,
        'time': 0.0,
        'wheels' : {
            'fl' : 0,
            'fr' : 0,
            'rl' : 0,
            'rr' : 0
        }
    }

    instructions = {
        'message' : '',
        'motor' : OFF,
        'steering' : CENTER,
        'brake' : OFF
    }

    recieved = {
        'message' : ''
    }

    def __init__(self, logger, options):
        self.logger = logger
        self.messaging = SerialMessaging(options, self.instructions['message'], self.recieved['message'])
        print(self.messaging.outbound)

    def info(self):
        ''' Return dictionary of Crawler status. '''
        return {
            "status": self.status,
        }


    def connect(self):
        ''' Establish serial connection with DE10. Initialize communication threads.'''
        print('Trying to connect to crawler')
        if self.messaging.connect():
            print('Created serial port.')
            print(str(self.messaging.connect))
            self.connected = self.messaging.authorize()
            #Use services if multi-threaded messaging is enabled
            #self.messaging.start_services()
            self.connected = True
        return self.connected


    def disconnect(self):
        ''' Disconnect from DE10. '''
        self.connected = False
        self.recieved = {'messsage' : ""}
        self.clear_instructions()
        self.messaging.disconnect()
        self.logger.debug('Crawler disconnected.')


    def clear_instructions(self):
        ''' Clear all instructions. '''
        self.instructions['message'] = ''
        self.instructions['motor'] = self.CENTER
        self.instructions['steering'] = self.CENTER
        self.instructions['brake'] = self.OFF


    def set_motor_instruction(self, motor):
        ''' Set the desired motor for the crawler motor. '''
        self.instructions['motor'] = str(-1*motor)


    def set_steering_instruction(self, x_axis):
        ''' Set desired steering instruction. '''
        #Smoothed steering instruction
        #self.instructions['steering'] = str(round(pow(64, x_axis)))
        self.instructions['steering'] = str(round(x_axis * 64))


    def set_brake_instruction(self, brake):
        ''' Set desired brake instruction. '''
        self.instructions['brake'] = str(brake)


    def set_instruction_message(self):
        ''' Set the instructions for the Crawler. '''
        print('setting message..')
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + '\r'
        self.messaging.set_message(self.instructions['message'])

    def send_message(self):
        self.messaging.send_message()

    def recieve_message(self):
        ''' Recieve message from de10. '''
        message, time = self.messaging.recieve_message()
        self.recieved['message'] = message
        self.recieved = time
        self.decode_recieved_message()
        return True


    def decode_recieved_message(self):
        return True

    def is_connected(self):
        ''' Returns True if Crawler is connected. '''
        return self.connected

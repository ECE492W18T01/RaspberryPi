''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import serial
from time import sleep
from modules.messaging import SerialMessaging


class Crawler():
    ON = 1
    OFF = 0
    CENTER = 0.0

    connected = False
    status = {
        'mode' : 0,
        'motors' : 0.0,
        'steering' : CENTER,
        'battery' : 0,

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


    def info(self):
        ''' Return dictionary of Crawler status. '''
        return {
            "status": self.status,
            "comm": self.comm
        }


    def connect(self):
        ''' Establish serial connection with DE10. Initialize communication threads.'''
        if self.messaging.connect():
            self.connected = self.messaging.authorize()
            
            
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
        self.instructions['steering'] = str(round(x_axis * 64))


    def set_brake_instruction(self, brake):
        ''' Set desired brake instruction. '''
        self.instructions['brake'] = str(brake)


    def set_instruction_message(self):
        ''' Set the instructions for the Crawler. '''
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + '\r'
        self.messaging.outbound = self.instructions['message']
        
    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        self.set_instructions()
        self.port.write(self.instructions['message'].encode())
        self.logger.info('Sent message: ' + self.instructions['message'])
        #self.clear_instructions()


    def recieve_message(self):
        ''' Recieve message from de10. '''
        self.recieved = self.messaging.inbound
        print(self.recieved)
        #self.logger.info('Recieved message: ' + self.recieved['message'])


    def decode_recieved_message(self):
        return true

    def is_connected(self):
        ''' Returns True if Crawler is connected. '''
        return self.connected

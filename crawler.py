''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import serial
from time import sleep
from modules.messaging import SerialMessaging
from math import pow
from queue import Queue
from io import StringIO
import csv

class Crawler():
    ON = 1
    OFF = 0
    CENTER = 0.0

    connected = False

    status = {
        'connected' : True,
        'message' : "Crawler not connected.",
        'brake' : 0,
        'distance' : 0,
        'last_updated': None,
        'motors' : {
            'fl' : 0,
            'fr' : 0,
            'rl' : 0,
            'rr' : 0,
            'steering' : 0
        },
        'sensors' : {
            'fl' : 0,
            'fr' : 0,
            'rl' : 0,
            'rr' : 0,
            'steering' : 0,
        },
        'fuzzy' : {
            'enabled': 0,
            'fl' : 0,
            'fr' : 0,
            'rl' : 0,
            'rr' : 0,
            'steering' : 0,
        }
    }

    instructions = {
        'message' : '',
        'motor' : OFF,
        'steering' : CENTER,
        'brake' : OFF
    }

    recieved = {
        'messages' : None
    }

    def __init__(self, logger, options):
        self.logger = logger
        self.recieved['messages'] = Queue()
        self.messaging = SerialMessaging(options, self.recieved['messages'])
        

    def get_status(self):
        ''' Return dictionary of Crawler status. '''
        return self.status


    def connect(self):
        ''' Establish serial connection with DE10. Initialize communication threads.'''
        print('Trying to connect to crawler')
        if self.messaging.connect():
            print('Created serial port.')
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
        #print('Setting message..')
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + '\r'
        self.messaging.set_message(self.instructions['message'])

    def send_message(self):
        self.messaging.send_message()

    def recieve_messages(self):
        ''' Recieve message from de10. '''
        #print('Recieving message.')
        self.messaging.recieve_messages()
        #print(self.recieved['messages'].qsize())
        #self.recieved['time'] = time
        self.set_crawler_status()
        return True


    def set_crawler_status(self):
        print('Updating Crawler Status.')
        while not self.recieved['messages'].empty():
            message = self.recieved['messages'].get()
            try:
                f = StringIO(message)
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    status = int(row[0])
                    if status == 1:
                        self.handle_sensor_message(row)
                    elif status == 2:
                        self.handle_fuzzy_message(row)
                    elif status == 3:
                        self.handle_distance_message(row)
                    elif status == 4:
                        self.handle_status_message(row)
                    elif status == 5:
                        self.handle_motor_message(row)
                    elif status == 6:
                        self.handle_toggle_message(row)
            except:
                print('Error handling message: ' + row)
        print(self.status)
        return True
    
    def handle_sensor_message(self, message):
        #print(message[0] + '. Hall sensor readings')
        #    1, fl, fr, rl, rr
        #ex. 1,0,0,0,0
        self.status['sensors']['fl'] = int(message[1])
        self.status['sensors']['rl'] = int(message[2])
        self.status['sensors']['rl'] = int(message[3])
        self.status['sensors']['rr'] = int(message[4])
        return True

    def handle_fuzzy_message(self, message):
        #print(message[0] + '. Fuzzy output message')
        #    2, fl, fr, rl, rr, steering
        #ex. 2,0.000000,0.000000,0.000000,0.000000,0
        self.status['fuzzy']['fl'] = message[1]
        self.status['fuzzy']['rl'] = message[2]
        self.status['fuzzy']['rl'] = message[3]
        self.status['fuzzy']['rr'] = message[4]
        self.status['fuzzy']['steering'] = message[5]
        return True
        
    def handle_distance_message(self, message):
        #    3, distance
        #ex. 3, 0
        self.status['distance'] = message[1]
        return True
        
    def handle_status_message(self, message):
        #print(message[0] + '. Status message')
        # Not implemented
        return True
        
    def handle_motor_message(self, message):
        #print(message[0] + '. Motor output message')
        #    5, fl, fr, rl, rr, steering
        #ex. 5,0.000000,0.000000,0.000000,0.000000,0
        self.status['motors']['fl'] = message[1]
        self.status['motors']['rl'] = message[2]
        self.status['motors']['rl'] = message[3]
        self.status['motors']['rr'] = message[4]
        self.status['motors']['steering'] = message[5]
        return True
        
    def handle_toggle_message(self, message):
        #print(message[0] + '. Toggle Message')
        #    6, ebrake, fuzzy
        #ex. 6, 0, 0
        self.status['brake'] = message[1]
        self.status['fuzzy']['enabled'] = message[2]
        return True

    def is_connected(self):
        ''' Returns True if Crawler is connected. '''
        return self.connected

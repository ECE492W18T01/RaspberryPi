''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import threading
import serial

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

    messages = {
        'connect' : "*",
        'disconnect' : "&",
        'ack' : "@"
    }

    instructions = {
        'message' : '',
        'motor' : OFF,
        'steering' : CENTER,
        'brake' : OFF
    }

    recieved = {}
    
    port = None
    comm = {
        "baudrate" : 115200,
        "timeout" : 3.0,
        "read_size" : 10,
        "instruction_freq" : 10,
        "connect_freq" : 1/10,
        "device" : '/dev/ttyUSB0', 
    }

    def info(self):
        ''' Return dictionary of Crawler status. '''
        return {
            "status": self.status,
            "comm": self.comm
        }

    def connect(self):
        ''' Establish serial connection with DE10 '''
        try:
            self.port = serial.Serial(self.comm['device'], baudrate=self.comm['baudrate'], timeout=self.comm['timeout'])
            self.port.write(self.messages['connect'].encode())
            self.recieved['message'] = self.port.read(10)
            print(self.recieved['message'].decode("utf-8"))
            if self.recieved['message'].decode("utf-8") is '@': 
                self.connected = True
                print('Connected to Crawler.')
            else:
                self.connected = False
                print("Can't connect to Crawler. Make sure device is connected.")
                
        except:
            print("Can't connect to Crawler. Make sure device is connected.")

    def disconnect(self):
        ''' Disconnect from DE10 '''
        self.port.write(self.messages['disconnect'].encode())
        self.connected = False
        self.comm.recieved = {}
        self.clear_instructions()
        print('Crawler disconnected.')

    def clear_instructions(self):
        ''' Clear all instructions '''
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
        
    def set_instructions(self):
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + ',' + str(self.instructions['brake']) + '\r'
        print(self.instructions['message'])

    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        self.set_instructions()
        self.port.write(self.instructions['message'].encode())
        self.clear_instructions()

    def recieve_instruction(self):
        ''' Recieve message from de10 '''
        self.recieved['message'] = self.port.read(self.comm['read_size'])
        
    def is_connected(self):
        return self.connected
        

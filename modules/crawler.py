''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import threading
import serial

class Crawler(threading.Thread):
    ON = 1
    OFF = 0
    CENTER = 0.0

    connected = 0
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
        'connect' : "S\r",
        'disconnect' : "E\r"
    }

    instructions = {
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


    def run(self):
        while True:
            self.connect()
            while self.connected == 1:
                self.send_instruction()
                ''' Recieving instructions
                self.recieve_instruction()
                if self.recieved == self.comm.end:
                    self.connect = 0
                '''
                sleep(1/self.comm['instruction_freq'])
            sleep(1/self.comm['connect_freq'])

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
            self.port.write(self.messages['start'].encode())
            self.recieved['message'] = self.port.read(self.comm['read_size'])
            
            self.connected = 1 
            print('Crawler connected on ', self.comm['device'])
        except:
            print("Can't connect to Crawler. Make sure device is connected.")

    def disconnect(self):
        ''' Disconnect from DE10 '''
        self.connected = 0
        self.comm.recieved = {}
        self.clear_instructions()

    def clear_instructions(self):
        ''' Clear all instructions '''
        self.instructions['motor'] = self.CENTER
        self.instructions['steering'] = self.CENTER
        self.instructions['brake'] = self.OFF

    def set_motor_instruction(self, motor):
        ''' Set the desired motor for the crawler motor. '''
        self.instructions['motor'] = str(-1*motor)

    def set_steering_instruction(self, x_axis):
        ''' Set desired steering instruction. '''
        self.instructions['steering'] = str(x_axis * 60)
        
    def set_brake_instruction(self, brake):
        ''' Set desired brake instruction. '''
        self.instructions['brake'] = str(brake)

    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        instructions = self.instructions['motor'] + ',' + self.instructions['steering'] + '\r'.encode()
        self.port.write(instructions)
        clear_instructions()

    def recieve_instruction(self):
        ''' Recieve message from de10 '''
        self.recieved['message'] = self.port.read(self.comm['read_size'])
        
    def is_connected(self):
        if self.connected == 1:
            return True
        else:
            return False

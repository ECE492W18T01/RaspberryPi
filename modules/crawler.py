''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
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

    instructions = {
        'message' : '',
        'motor' : OFF,
        'steering' : CENTER,
        'brake' : OFF
    }

    recieved = {}

    port = None
    messages = {}
    comm = {}

    def __init__(self, logger, messages, communication):
        self.logger = logger
        self.configure_messages(messages)
        self.configure_communication(communication)

    def configure_messages(self, messages):
        self.messages['connect'] = messages['Connect']
        self.messages['disconnect'] = messages['Disconnect']
        self.messages['ack'] = messages['Acknowledgement']

    def configure_communication(self, communication):
        self.comm['baudrate'] = int(communication['Baudrate'])
        self.comm['timeout'] = float(communication['Timeout'])
        self.comm['read_size'] = int(communication['ReadSize'])
        self.comm['instruction_freq'] = float(communication['InstructionFrequency'])
        self.comm['connect_freq'] = float(communication['ConnectFrequency'])
        self.comm['device'] = communication['Device']

    def info(self):
        ''' Return dictionary of Crawler status. '''
        return {
            "status": self.status,
            "comm": self.comm
        }

    def connect(self):
        ''' Establish serial connection with DE10. '''
        self.port = serial.Serial(device=self.comm['device'], baudrate=self.comm['baudrate'], timeout=self.comm['timeout'])
        self.port.write(self.messages['connect'].encode())
        self.recieved['message'] = self.port.read(self.comm['read_size'])
        self.logger.debug(self.recieved['message'].decode("utf-8"))
        if self.recieved['message'].decode("utf-8") is self.messages['ack']:
            self.connected = True
            self.logger.info('Connected to Crawler.')
        else:
            self.connected = False
            self.logger.info("Can't connect to Crawler. Make sure device is connected.")


    def disconnect(self):
        ''' Disconnect from DE10. '''
        self.port.write(self.messages['disconnect'].encode())
        self.connected = False
        self.comm.recieved = {}
        self.clear_instructions()
        self.logger.info('Crawler disconnected.')


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


    def set_instructions(self):
        ''' Set the instructions for the Crawler. '''
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + ',' + str(self.instructions['brake']) + '\r'


    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        self.set_instructions()
        self.port.write(self.instructions['message'].encode())
        self.logger.info('Sent message: ' + self.instructions['message'])
        self.clear_instructions()


    def recieve_instruction(self):
        ''' Recieve message from de10. '''
        self.recieved['message'] = self.port.read(self.comm['read_size'])
        self.logger.info('Recieved message: ' + self.recieved['message'])


    def is_connected(self):
        ''' Returns True if Crawler is connected. '''
        return self.connected

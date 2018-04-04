''' Crawler Module

High Level interface to the Smart Tank Crawler.

TODO:
- Implement serial connection failure protocols.
'''
import serial
from time import sleep
from messaging import OutboundMessaging, InboundMessaging

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
        ''' Establish serial connection with DE10. Initialize communication threads.'''
        self.port = serial.Serial(self.comm['device'], baudrate=115200, timeout=3.0)
        sleep(0.5)
        self.port.flushInput()
        self.port.flushOutput()
        sleep(0.5)
        self.port.write(self.messages['connect'].encode())
        sleep(0.5)
        self.outbound_messaging = OutboundMessaging(self.port, 0.1, self.instructions['message'])
        self.inbound_messaging = InboundMessaging(self.port, 0.2, self.recieved['message'])
        #self.recieved['message'] = self.port.read(self.comm['read_size'])
        #self.logger.debug(self.recieved['message'].decode("utf-8"))
        #print(self.recieved['message'].decode("utf-8"))
        #print(self.messages['ack'])
        self.connected = True
        '''
        if self.recieved['message'].decode("utf-8") is self.messages['ack']:
            self.connected = True
            self.logger.debug('Connected to Crawler.')
            return True
        else:
            self.connected = False
            self.logger.debug("Can't connect to Crawler. Make sure device is connected.")
            return False
            '''


    def disconnect(self):
        ''' Disconnect from DE10. '''
        if self.port is not None:
            self.port.write(self.messages['disconnect'].encode())
        self.connected = False
        self.recieved = {}
        self.clear_instructions()
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


    def set_message(self):
        ''' Set the instructions for the Crawler. '''
        self.instructions['message'] = str(self.instructions['motor']) + ',' + str(self.instructions['steering']) + '\r'
        self.outbound_messaging.set_message(self.instructions['message'])

    def send_instructions(self):
        ''' Send instructions via the connected serial port. '''
        self.set_instructions()
        self.port.write(self.instructions['message'].encode())
        self.logger.info('Sent message: ' + self.instructions['message'])
        #self.clear_instructions()


    def recieve_message(self):
        ''' Recieve message from de10. '''
        self.inbound_messaging.get_message()
        print('Recieved.')
        #self.logger.info('Recieved message: ' + self.recieved['message'])


    def is_connected(self):
        ''' Returns True if Crawler is connected. '''
        return self.connected

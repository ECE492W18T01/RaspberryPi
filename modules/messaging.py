import threading


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
        return True
    
    def send_messsage(self, message):
        self.port.write(message.encode())
        return True

    def set_message(self, message):
        this.message = message.encode()
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
        return True
    
    def read_message(self):
        message = self.port.read(self.read_size)
        return message

    def get_message(self):
        return this.message
    
    def get_status(self):
        return this.status
    
class SerialMessaging():
    connect = "*"
    disconnect = "&"
    acknowledgment = "@"
    port = None
    
    is_connected = False
    
    
    def __init__(self, options, outbound, inbound):
        self.options = options
        self.configure(options)
        self.outbound = outbound
        self.inbound = inbound
        
    def connect(self):
        ''' Attempt to create serial port for communication. '''
        try:
            self.port = serial.Serial(self.device, baudrate=self.baudrate, timeout=self.timeout)
            self.outbound = OutboundMessaging(self.port, 0.1, outbound)
            self.inbound = InboundMessaging(self.port, 0.2, inbound)
            self.is_connected = True
            return True
        except:
            print('Failed to create serial port. Check connection.')
            self.is_connected = False
            return False
        
    def authorize(self):
        ''' Authorize communication with Crawler. '''
        this.port.write(self.connect.encode())
        sleep(0.1)
        msg = this.port.read(128).decode()
        if msg == self.acknowledgment:
            return True
        else:
            return False
        
    
    def disconnect(self):
        if self.port is not None:
            self.port.write(self.messages['disconnect'].encode())
            self.port.disconnect()
        return True
    
    def start_communication():
        self.outbound.start()
        self.inbound.start()
        
    def configure(self, options):
        self.baudrate = int(options['Baudrate'])
        self.timeout = float(options['Timeout'])
        self.device = options['Device']
        return True
    
    def test(self):
        print('Testing')
        return True
        
    
    

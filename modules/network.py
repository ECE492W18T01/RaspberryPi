#Network Class
import urllib2

class Network:
    self.enable = False
    self.host = 'localhost'
    self.port = 8080
    self.connection = None
    self.client = None

    def __init__(self, enable, host, port):
        self.enable = enable
        self.host = host
        self.port = port

    def connect(self):
        if self.enable:
            self.client = socket.socket()
            print 'Attempting to connect to %s:%d...' % (self.host, self.port)
            self.client.connect((self.host, self.port))
            self.connection = self.client.makefile('wb')
            print 'Connected.'
        else:
            print('Network is disabled. Try enabling first.')

    def send(self, data):
        if self.enable:
            print('Sending data...')
        else:
            print('Network is disabled. Try enabling first.')

    def finish():
        if self.connection is not None:
            self.connection.close()
            self.client.close()
            print 'Disconnected from %s:%d.' % (self.host, self.port)

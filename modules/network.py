''' Network module

Currently unused by the application.

TODO:
- implement high level streaming class (optional).
'''

class Network:
    enable = False
    host = 'localhost'
    port = 8080
    connection = None
    client = None


    def connect(self):
        if self.enable:
            self.client = socket.socket()
            print('Attempting to connect to %s:%d...') % (self.host, self.port)
            self.client.connect((self.host, self.port))
            self.connection = self.client.makefile('wb')
            print('Connected.')
        else:
            print('Network is disabled. Try enabling first.')

    def send(self, data):
        if self.enable:
            print('Sending data...')
        else:
            print('Network is disabled. Try enabling first.')

    def finish(self):
        if self.connection is not None:
            self.connection.close()
            self.client.close()
            print('Disconnected from %s:%d.') % (self.host, self.port)

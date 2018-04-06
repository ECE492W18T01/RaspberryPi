from io import BytesIO
import socket
import struct

class StreamingClient():
    SEND_FREQUENCY = 0.5
    CONNECT_FREQUENCY = 0.1

    def __init__(self, host, port, stream):
        self.host = host
        self.port = port
        self.stream = stream

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.connection = self.socket.makefile('wb')

    def authorize(self):
        return True

    def stream_data(self, frequency):
        self.connection.write(struct.pack('<L', self.stream.tell()))
        self.connection.flush()
        self.stream.seek(0)
        self.frame = self.connection.write(self.stream.read())
        print(self.frame)
        self.stream.seek(0)
        self.stream.truncate()
        time.sleep(1/frequency)

    def end_session(self):
        self.connection.write(struct.pack('<L', 0))
        self.connection.close()
        self.socket.close()

    def run(self):
        while True:
            self.connect()
            if self..authorize():
                try:
                    self.stream_data(self.send_frequency)
                except:
                    self.end_session()
            sleep(self.connect_frequency)

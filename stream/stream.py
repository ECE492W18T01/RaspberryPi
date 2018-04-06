import socket
from time import sleep
import logging
from io import BytesIO
from threading import Condition
import threading
import socketserver
import struct
from http import server
import os
import PIL
from PIL import Image
from modules.frame import Frame

#web_dir = os.path.join(os.path.dirname(__file__))
#os.chdir(web_dir)


class StreamingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass):
        TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.frame = frame
        self.buffer = BytesIO()
        self.condition = Condition()
        self.port = 8080
        self.connected = False
        self.sample = ""


    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            frame.write_new_Frame(self.buffer.getvalue())
            self.buffer.seek(0)
        return self.buffer.write(buf)

    def connect(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(0)
        print('Waiting for stream.')
        self.connection = self.server_socket.accept()[0].makefile('rb')
        self.connected = True
        print('Streaming Connection accepted. Streaming now.')

    def disconnect(self):
        self.connected = False
        self.connection.close()
        self.server_socket.close()
        print('Disconnected.')

    def read(self):
        try:
            chunk_length = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            print(chunk_length)
            self.sample = self.connection.read(chunk_length)
            self.write(self.sample)
            self.verify()
        except:
            self.disconnect()

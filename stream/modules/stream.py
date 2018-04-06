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

#web_dir = os.path.join(os.path.dirname(__file__))
#os.chdir(web_dir)

class Stream(threading.Thread, object):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.buffer = BytesIO()
        self.condition = Condition()
        self.port = 8080
        self.connected = False
        self.sample = ""

    def run(self):
        while True:
            self.connect()
            while self.connected:
                self.read()
            sleep(5)

    def view_stream(self):
        if self.connected:
            return self.frame
        else:
            return False

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
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
            self.sample = self.connection.read(chunk_length)
            self.write(self.sample)
        except:
            self.disconnect()


class StreamHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/index.html':
            content = "Hello".encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        if self.path == '/stream.mjpeg':
            print('Stream request')
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            stream = Stream()
            stream.start()
            try:
                while True:
                    print('.')
                    with stream.condition:
                        stream.condition.wait()
                        frame = stream.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

class StreamingServer(server.HTTPServer, server.BaseHTTPRequestHandler):

    def __init__(self, server_address, RequestHandlerClass):
        server.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.port = server_address[1]

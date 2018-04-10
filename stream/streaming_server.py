import socket
from time import sleep
import logging
from io import BytesIO
from threading import Condition
import threading
import socketserver
import struct
import os
import PIL
from PIL import Image
from modules.frame import Frame


#web_dir = os.path.join(os.path.dirname(__file__))
#os.chdir(web_dir)

class Stream(threading.Thread):
    def __init__(self, connection, frame):
        threading.Thread.__init__(self)
        self.connection = connection
        self.frame = frame
        self.buffer = BytesIO()

    def run(self):
        while True:
            try:
                self.read()
            finally:
                sleep(1)

    def read(self):
        try:
            chunk_length = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            print(chunk_length)
            self.sample = self.connection.read(chunk_length)
            self.write(self.sample)
        finally:
             sleep(0.5)

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            self.frame.write_frame(self.buffer.getvalue())
            self.frame.save_frame_as_jpeg('frame.jpeg')
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(threading.Thread):
    PAGE ="""\
            <html>
            <head>
            <title>picamera MJPEG streaming demo</title>
            </head>
            <body>
            <h1>PiCamera MJPEG Streaming Demo</h1>
            <img src="stream.mjpg" width="640" height="480" />
            </body>
            </html>
            """


    def __init__(self, request, socket, frame):
        threading.Thread.__init__(self)
        self.frame = frame
        self.socket = socket
        self.request = request

    def run(self):
        self.handle_request()

    def handle_request(self):
        self.send_response(200)
        '''
        content = self.PAGE.encode()
        self.socket.send('Content-Type: text/html'.encode())
        content_length_header = 'Content-Length: ' + str(len(content)) + '\r\n\r\n'
        self.socket.send(content_length_header.encode())
        self.socket.send(content)
        '''
        self.send_response_header()
        self.socket.send('Waiting for stream..'.encode())
        try:
            while True:
                print('.')
                with self.frame.condition:
                    self.frame.condition.wait()
                    frame = self.frame.frame
                print('Frame available')
                self.write_frame_to_connection(self.socket, frame)
        finally:
            print('Stream has ended.')


    def write_frame_to_connection(self, socket, frame):
        boundary = '--frame\r\n'
        frame_header = 'Content-Type: image/jpeg\r\n\r\n'
        data = ('%s %s %s') % (boundary, frame_header, frame)
        print(data)
        self.socket.send(data.encode())

    def send_response(self, status):
        proto = 'HTTP/1.1'
        status = 200
        text = 'OK'
        response = ('%s %d %s\r\n') %(proto, status, text)
        print(response)
        self.socket.send(response.encode())
        return True


    def send_response_header(self):
        response_header = 'Content-Type: multipart/x-mixed-replace; boundary=frame'
        print(response_header)
        self.socket.send(response_header.encode())


class StreamingServer():

    def __init__(self):
        self.frame = Frame()
        self.condition = Condition()
        self.port = 8080
        self.connected = False
        self.sample = ""
        self.max_sockets = 1024
        self.stream_id = b'12345'
        self.threads = []

    def serve_forever(self, poll_frequency=0.5):
        while True:
            print('Waiting for connection.')
            self.server_socket.listen(self.max_sockets)
            (client_socket, address) = self.server_socket.accept()
            print(address)
            self.authenticate(client_socket)
            sleep(1/poll_frequency)
        return True

    def connect(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.port))

    def authenticate(self, socket):
        size = 5
        read_write = 'rb'
        connection = socket.makefile(read_write)
        request = connection.read(size)
        print(request)
        if request == self.stream_id:
            self.handle_stream(connection)
        else:
            self.handle_request(request, socket)

    def handle_request(self, request, socket):
        handler = StreamingHandler(request, socket, self.frame)
        handler.start()


    def handle_stream(self, connection):
        print('Stream request.')
        self.stream_connection = connection
        self.stream = Stream(connection, self.frame)
        self.stream.start()

    def disconnect(self):
        self.connected = False
        self.connection.close()
        self.server_socket.close()
        print('Disconnected.')

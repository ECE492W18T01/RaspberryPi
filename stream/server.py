from io import BytesIO
import socket
import struct
import threading
from time import sleep
from PIL import Image
import modules.streaming as Streaming

class Server(threading.Thread):
        def __init__(self, name):
            threading.Thread.__init__(self)
            self.name = name

        def run(self):
            try:
                print('Server here')
                sleep(100)
                #address = ('', 8080)
                #server = Streaming.Server(address, Streaming.Handler)
                #server.serve_forever()
            finally:
                connection.close()
                server_socket.close()


class CaptureStream(threading.Thread):
        def __init__(self, name):
            threading.Thread.__init__(self)
            self.name = name

        def run(self):
            while True:
                chunk_length = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                print(chunk_length)
                stream = Streaming.Output()
                stream.write(connection.read(chunk_length))


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
print('Listening at 0.0.0.0:8000')

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

server_thread = Server('Streaming Server')
stream_thread = CaptureStream('Capture Stream')


server_thread.start()
stream_thread.start()

server_thread.join()
stream_thread.join()

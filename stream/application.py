from io import BytesIO
import socket
import struct
import threading
from PIL import Image
import modules.streaming as Streaming

class Server(threading.Thread):
        def __init__(self, name, frequency):
            threading.Thread.__init__(self)
            self.name = name
            self.frequency = frequency

        def run(self):
            try:
                address = ('', 8080)
                server = Streaming.Server(address, Streaming.Handler)
                server.serve_forever()
            finally:
                connection.close()
                server_socket.close()


class CaptureStream(threading.Thread):
        def __init__(self, name, frequency):
            threading.Thread.__init__(self)
            self.name = name
            self.frequency = frequency

        def run(self):
            while True:
                chunk_length = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                print(chunk_length)
                if not chunk_length:
                    break
                stream = Streaming.Output()
                stream.write(connection.read(chunk_length))
                ##time.sleep(1/self.frequency)


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
print('Listening at 0.0.0.0:8000')

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

RESPONSE_FREQUENCY = 0
server_thread = Server('Server', RESPONSE_FREQUENCY)
STREAM_FREQUENCY = 0
stream_thread = CaptureStream('Stream', STREAM_FREQUENCY)


server_thread.start()
stream_thread.start()

server_thread.join()
stream_thread.join()

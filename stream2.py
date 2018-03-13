from io import BytesIO
import socket
import struct
import time
from picamera import PiCamera
import modules.streaming as Streaming

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
aws_url = 'http://crawler-stream.us-west-2.elasticbeanstalk.com/'
home_url = '192.168.0.3'
port = 8000

client_socket = socket.socket()
client_socket.connect((home_url, 8000))
connection = client_socket.makefile('wb')

try:
    start = time.time()
    
    with PiCamera(resolution='640x480', framerate=24) as camera:
        stream = BytesIO()
        camera.start_recording(stream, format='mjpeg')
    
        while True:
            print(stream.tell())
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            
            if time.time() - start > 30:
                break
            
            stream.seek(0)
            stream.truncate()
        
        connection.write(struct.pack('<L', 0))
        

finally:
    connection.close()
    client_socket.close()


from io import BytesIO
import socket
import struct
import time
from picamera import PiCamera
import modules.stream as Streaming
import PIL.Image as Image

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
aws_url = 'http://crawler-stream.us-west-2.elasticbeanstalk.com/'
home_url = '192.168.0.5'
port = 8080


client_socket = socket.socket()
client_socket.connect((home_url, port))
connection = client_socket.makefile('wb')

try:
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        time.sleep(2)
        start = time.time()
        count = 0
        stream = BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            frame = connection.write(stream.read())
            print(frame)
            count += 1
            if time.time() - start > 30:
                break
            stream.seek(0)
            stream.truncate()
            time.sleep(6)

    connection.write(struct.pack('<L', 0))


finally:
    connection.close()
    client_socket.close()
    finish = time.time()

    print('Sent %d images in %d seconds at %.2ffps' %(count, finish-start, count/(finish-start)))

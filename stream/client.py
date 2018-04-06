from io import BytesIO
import socket
import struct
from time import sleep
from picamera import PiCamera


port = 8080
#host = 'http://crawler-stream.us-west-2.elasticbeanstalk.com/'
host = '192.168.0.5'
format = 'jpeg'

while True:
    client.connect()
    if client.authorize():

        with PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 30
            stream = BytesIO()
            client = StreamingClient(host, port, stream)

            for frame in camera.capture_continuous(stream, format, use_video_port=True):
                try:
                    client.stream_data(client.SEND_FREQUENCY)
                except:
                    client.end_session()
            sleep(client.CONNECT_FREQUENCY)

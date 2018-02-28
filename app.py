import io
import socket
import struct
import time
import picamera

client = socket.socket()
client.connect(('localhost', 8080))

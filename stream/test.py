from io import BytesIO
import socket
import struct
import threading
import logging
from http import server
from time import sleep
from modules.stream import Stream, StreamHandler, StreamingServer
from flask import Flask
from PIL import Image



stream = Stream()
stream.start()

while True:
    try:
        sample = stream.view_stream()
        if sample is not False:
            image = Image.open(sample)
    except:
        print('Didnt work')
    finally:
        sleep(1)

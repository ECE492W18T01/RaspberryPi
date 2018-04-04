from io import BytesIO
import socket
import struct
import threading
import logging
from http import server
from time import sleep
from modules.stream import Stream, StreamHandler, StreamingServer
from flask import Flask

app = Flask(__name__)


format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server.py')
logger.setLevel('INFO')
fh = logging.FileHandler('server.log')
fh.setFormatter(format)
logger.addHandler(fh)


address = ('', 8000)
'''
stream = Stream()
stream.start()
'''
handler = StreamHandler
streaming_server = StreamingServer(address, handler)

streaming_server.serve_forever()

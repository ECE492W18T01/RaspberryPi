from io import BytesIO
import socket
import struct
import threading
import logging
from time import sleep
from stream import Stream, StreamingServer
from flask import Flask, render_template, Response
import PIL
from PIL import Image
from flask_socketio import SocketIO
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

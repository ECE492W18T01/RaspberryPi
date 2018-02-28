import io
import socket
import struct
import time
import picamera
import pygame

pygame.init()

client = socket.socket()
client.connect(('localhost', 8080))

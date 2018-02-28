import io
import socket
import struct
import time
from modules.controller import DS4
from modules.crawler import Crawler

#Network Variables
NETWORK_ENABLED = 0
HOST = 'localhost'
PORT = 8080

#Initilize Peripherals
controller = DS4()
controller.connect()

crawler = Crawler()
crawler.connect()

#Build connection object and connect
if NETWORK_ENABLED:
    client = socket.socket()
    print 'Connecting to %s:%d' % (HOST, PORT)
    client.connect((HOST, PORT))
    connection = client.makefile('wb')
    print 'Connected'

try:
    while True:
        #Send camera data across network
        if NETWORK_ENABLED:
            print('Sending stream over network')

        #Recieve controller input
        commands = controller.get_input()

        #Output controller input to GPIO
        crawler.set_motor(commands.acceleration)
        crawler.set_steering(commands.steering)

finally:
    if NETWORK_ENABLED:
        connection.close()
        client.close()
        print 'Disconnected from %s:%d' % (HOST, PORT)
    controller.disconnect()
    crawler.disconnect()

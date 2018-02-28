import io
import socket
import struct
import time


#Network Variables
HOST = 'localhost'
PORT = 8080

#STATUS
MOTORS = ON
STEERING = 0

#Build connection object and connect
client = socket.socket()
print 'Connecting to %s:%d' % (HOST, PORT)
client.connect((HOST, PORT))
connection = client.makefile('wb')
print 'Connected'

try:
    while True:
        #Send camera data across network


        #Recieve controller input
        commands = controller.get_input()
        MOTOR_STATUS = commands.acceleration
        STEERING = commands.steering

        #Output controller input to GPIO

        print('.')
        time.sleep(5)

finally:
    connection.close()
    client.close()
    print 'Disconnected from %s:%d' % (HOST, PORT)

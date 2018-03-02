#Crawler class
import RPi.GPIO as GPIO
import serial

class Crawler:
    ON = 1
    OFF = 0
    CENTER = 0.0
    BAUDRATE = 11520
    TIMEOUT = 3.0
    READ_SIZE = 10

    motor = 0
    steering = CENTER

    wheels = {
        'fl' : 0,
        'fr' : 0,
        'rl' : 0,
        'rr' : 0
    }

    battery = 0

    def connect(self):
        try:
            port = serial.Serial("/dev/serial0", baudrate=self.BAUDRATE, timeout=self.TIMEOUT)
            print('Crawler connected on serial0')
            break
        except TimeoutError():
            print("Cannot connect to crawler")


    def set_motor(self, mode):
        self.motor = mode


    def set_steering(self, steering):
        self.steering = steering


    def send_instructions(self):
        try:
            port.write("%d, %d") % (self.motor, self.steering)
            recieved = port.read(READ_SIZE)
            print("Recieved")
        except TimeoutError():
            print("Timeout occured")

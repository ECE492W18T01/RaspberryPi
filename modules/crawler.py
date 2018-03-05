#Crawler class
#import RPi.GPIO as GPIO
import serial

class Crawler:
    ON = 1
    OFF = 0
    CENTER = 0.0
    BAUDRATE = 11520
    TIMEOUT = 3.0
    READ_SIZE = 10

    port = None

    motor = 0
    steering = CENTER

    wheels = {
        'fl' : 0,
        'fr' : 0,
        'rl' : 0,
        'rr' : 0
    }

    battery = 0
    
    def info(self):
        return {
            'baudrate' : self.BAUDRATE,
            'motor' : self.motor,
            'wheels' : self.wheels
            }

    def connect(self):
        self.port = serial.Serial("/dev/serial0", baudrate=self.BAUDRATE, timeout=self.TIMEOUT)
        print('Crawler connected on serial0')

    def set_motor(self, mode):
        self.motor = mode


    def set_steering(self, steering):
        self.steering = steering


    def send_instructions(self):
        self.port.write("%d, %d") % (self.motor, self.steering)
        recieved = self.port.read(READ_SIZE)
        print("Recieved")

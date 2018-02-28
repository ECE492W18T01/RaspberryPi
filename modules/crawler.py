#Crawler class
import RPi.GPIO as GPIO

ON = 1
OFF = 0

CENTER = 0
LEFT = -180
RIGHT = 180

MOTOR_PIN = 24
STEERING_PIN = 26

class Crawler:
    motor = 0
    steering = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_PIN, GPIO.OUT)
        GPIO.setup(STEERING_PIN, GPIO.OUT)
        print('Crawler connected')

    def set_motor(self, command):
        self.motor = command
        GPIO.output(MOTOR_PIN, self.motor)

    def set_steering(self, command):
        self.steering = command
        GPIO.output(STEERING_PIN, self.steering)

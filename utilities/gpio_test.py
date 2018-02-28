import RPi.GPIO as GPIO

output_pin = 24
ON = 1
OFF = 0

from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(output_pin, ON)
        sleep(0.5)
        GPIO.output(output_pin, OFF)
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

from module.controller import DS4
from module.crawler import Crawler
from module.network import Network
from picamera import PiCamera

print('Camera preview started..')
camera = PiCamera()
camera.start_preview()
sleep(20)
camera.stop_preview()
print('Camera preview ended..')

sleep(5)

print("Controller test started..")
controller = DS4()
controller.connect()
print(controller.name)
testing = 40
try:
    while testing > 0:
        instruction = "R2: " + controller.get_button(controller.R2)
        instruction = instruction + ", X: ", controller.get_axis()[controller.LEFT_X_AXIS]
        print(instruction)
        sleep(0.5)
        testing = testing - 1

except KeyboardInterrupt:
    testing = False

finally:
    controller.disconnect()
    print("Controller test ended.")

<<<<<<< HEAD
from modules.controller import DS4
from modules.crawler import Crawler
from modules.network import Network
=======
''' IO Demo Script

Used during IO demonstration. Demonstrates the following:
- 20 second camera preview. Requires a monitor be connected to the Raspberry Pi.
- 20 second controller preview. Requires the dualshock 4 controller to be connected.

TODO:
- Add web streaming to demo (optional).
- Add crawler communication to demo (optional).
'''

from module.controller import DS4
from module.crawler import Crawler
from module.network import Network
>>>>>>> 2fffcd999ee4fd479749b80e76329711db53cb90
from picamera import PiCamera
from time import sleep

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
testing = 100
try:
    while testing > 0:
        r2 = controller.get_button(controller.R2)
        instruction1 = "R2: " + str(r2)
        left_x_axis = controller.get_axis()[controller.LEFT_X_AXIS]
        instruction2 = "X: " + str(left_x_axis)
        print(instruction1 + ", " + instruction2)
        sleep(0.1)
        testing = testing - 1

except KeyboardInterrupt:
    testing = False

finally:
    controller.disconnect()
    print("Controller test ended.")

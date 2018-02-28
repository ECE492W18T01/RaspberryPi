from modules.controller import DS4
from modules.crawler import Crawler

controller = DS4()
crawler = Crawler()

#Recieve controller input
commands = controller.get_input()

#Output controller input to GPIO
crawler.set_motor(commands.acceleration)
crawler.set_steering(commands.steering)

controller.disconnect()
crawler.disconnect()

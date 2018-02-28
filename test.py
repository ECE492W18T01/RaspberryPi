from modules.controller import DS4
from modules.crawler import Crawler

controller = DS4()
controller.connect()
print(controller.name)

crawler = Crawler()

commands = controller.get_input()
crawler.set_motor(commands['acceleration'])
crawler.set_steering(commands['steering'])

controller.disconnect()
crawler.disconnect()

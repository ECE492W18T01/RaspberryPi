import pygame
from modules.controller import DS4

controller = DS4()

commands = controller.get_input()
print(commands)

controller.disconnect()

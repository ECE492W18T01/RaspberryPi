''' Controller Module

Available Controllers:
- Dualshock 4 (DS4)

Requires:
- Pygame module
- Connected bluetooth controller

TODO:
- Check that controller is connected.
- Implement controller disconnect procedure.
'''

import pygame
from time import sleep

class DS4:
    joystick = None
    name = None
    axes_count = 0
    axes = {}
    buttons = {}
    connected = False

    CONNECT_FREQUENCY = 1/10

    SQUARE = 0
    X = 1
    CIRCLE = 2
    TRIANGLE = 3
    L1 = 4
    R1 = 5
    L2 = 6
    R2 = 7

    LEFT_X_AXIS = 0
    LEFT_Y_AXIS = 1
    RIGHT_X_AXIS = 2
    RIGHT_Y_AXIS = 5


    def connect(self):
        ''' Initiate pygame and pygame.joystick module used for the controller. '''
        try:
            pygame.init()
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.name = self.joystick.get_name()
            self.axes_count = self.joystick.get_numaxes()
            for i in range (0,self.axes_count):
                self.axes[i] = 0.0
            self.connected = True
            print(self.name, ' is connected.')
        except:
            self.connected = False
            print('No controller connected.')
            sleep(10)


    def get_button(self, button):
        ''' Return the value of button from the controller.

        Keyword arguments:
        button -- integer value associated with dualshock 4 controller button (default=self.R2)
        '''
        return self.joystick.get_button(button)


    def get_axes(self):
        ''' Return the value of all axes from the controller. '''
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axes[event.axis] = round(event.value, 2)
        return self.axes
    
    
    def is_connected(self):
        return self.connected


    def disconnect(self):
        ''' Quit the pygame module. '''
        pygame.quit()

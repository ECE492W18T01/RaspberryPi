#Dualshock 4 class
import pygame

class DS4:
    joystick = None
    name = None
    axis_count = 0
    axis = {}
    buttons = {}

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
    LEFT_Y_AXIS = 3


    def connect(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.name = self.joystick.get_name()
        self.axis_count = self.joystick.get_numaxes()
        for i in range (0,self.axis_count):
            self.axis[i] = 0.0


    def get_button(self, button):
        return self.joystick.get_button(button)


    def get_axis(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis[event.axis] = round(event.value, 2)
        return self.axis


    def disconnect(self):
        pygame.quit()

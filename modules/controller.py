#Dualshock 4 class
import pygame

class DS4:
    name = None
    joystick = None

    SQUARE = 0
    X = 1
    CIRCLE = 2
    TRIANGLE = 3
    L1 = 4
    R1 = 5
    L2 = 6
    R2 = 7

    X_AXIS = 3
    Y_AXIS = 4


    def connect(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.name = self.joystick.get_name()

    def get_input(self, button):
        return self.joystick.get_button(button)


    def get_input_buttons(self):
        return {
            'square' : self.joystick.get_button(self.SQUARE),
            'x' : self.joystick.get_button(self.X),
            'circle' : self.joystick.get_button(self.CIRCLE),
            'triangle' : self.joystick.get_button(self.TRIANGLE),
            'l1' : self.joystick.get_button(self.L1),
            'r1' : self.joystick.get_button(self.R1),
            'l2' : self.joystick.get_button(self.L2),
            'r2' : self.joystick.get_button(self.R2),
        }


    def get_input_axis(self):
        axis = {}
        axis[X_AXIS] = 0.0
        axis[Y_AXIS] = 0.0
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis[event.axis] = round(event.value, 2)

        return {
            'x' : axis['X_AXIS'],
            'y' : axis['Y_AXIS'],
        }


    def disconnect(self):
        pygame.quit()

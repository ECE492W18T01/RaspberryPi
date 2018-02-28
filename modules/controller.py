#Dualshock 4 class
import pygame

class DS4:
    name = None
    r2 = 7
    lr_axis = 1
    joystick = None

    def connect(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.name = self.joystick.get_name()

    def get_input(self):
        return {
            'acceleration' : self.get_acceleration(),
            'steering' : self.get_steering()
        }

    def get_acceleration(self):
        return self.joystick.get_button(self.r2)

    def get_steering(self):
        return self.joystick.get_axis(self.lr_axis)

    def disconnect(self):
        pygame.quit()

#Dualshock 4 class
import pygame

class DS4:
    R2 = 7
    LR_AXIS = 1

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
        #return self.joystick.get_button(self.R2)
        return 1

    def get_steering(self):
        #return self.joystick.get_axis(self.LR_AXIS)
        return 180

    def disconnect(self):
        pygame.quit()

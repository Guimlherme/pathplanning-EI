from .command import Forward, Stopped, Turn

class CommandFactory:
    def __init__(self, actuators):
        self.actuators = actuators

    def stopped(self):
        return Stopped(self.actuators)

    def forward(self, line_angle):
        return Forward(self.actuators, line_angle)

    def turn(self, side):
        return Turn(self.actuators, side)
from .command import Forward, Stopped, HalfTurn

class CommandFactory:
    def __init__(self, actuators):
        self.actuators = actuators

    def stopped(self):
        return Stopped(self.actuators)

    def forward(self, line_angle):
        return Forward(self.actuators, line_angle)

    def half_turn(self):
        return HalfTurn(self.actuators)
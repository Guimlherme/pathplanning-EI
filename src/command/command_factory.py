from .command import Forward, Stopped, RightTurn, LeftTurn

class CommandFactory:
    def __init__(self, actuators, simulation=False):
        self.actuators = actuators
        self.stopped_command = Stopped(self.actuators)
        self.forward_command = Forward(self.actuators, simulation)
        self.left_turn_command = LeftTurn(self.actuators)
        self.right_turn_command = RightTurn(self.actuators)

    def stopped(self):
        return self.stopped_command 

    def forward(self, line_angle):
        return self.forward_command 

    def left_turn(self):
        return self.left_turn_command 
    
    def right_turn(self):
        return self.right_turn_command 
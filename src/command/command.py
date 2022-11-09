RIGHT = 1
LEFT = -1

class Command:
    def get_name(self):
        return "Abstract Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self):
        self.actuators.set_speeds(0, 0)
    
    def get_name(self):
        return "Stopped"

class Turn(Command):
    def __init__(self, actuators, side):
        self.actuators = actuators
        self.side = side

    def execute(self):
        if self.side == RIGHT:
            self.actuators.set_speeds(1, -1)
        else:
            self.actuators.set_speeds(-1, 1)

    def get_name(self):
        return "Turn"

class Forward(Command):
    def __init__(self, actuators, angle):
        self.line_angle = angle
        self.actuators = actuators

    def execute(self):
        self.actuators.set_speeds(0.91, 1)
    
    def get_name(self):
        return "Forward"

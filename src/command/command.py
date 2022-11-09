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

class HalfTurn(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self):
        self.actuators.set_speeds(1, 1)
        # TODO: really do a half turn

    def get_name(self):
        return "HalfTurn"

class Forward(Command):
    def __init__(self, actuators, angle):
        self.line_angle = angle
        self.actuators = actuators

    def execute(self):
        self.actuators.set_speeds(1, 1)
    
    def get_name(self):
        return "Forward"

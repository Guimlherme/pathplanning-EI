RIGHT = 1
LEFT = -1

class Command:
    def get_name(self):
        return "Abstract Command"

    def execute(self, state):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        self.actuators.set_speeds(0, 0)
    
    def get_name(self):
        return "Stopped"

class LeftTurn(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        self.actuators.set_speeds(-1, 1)

    def get_name(self):
        return "LeftTurn"

class RightTurn(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        self.actuators.set_speeds(1, -1)

    def get_name(self):
        return "RightTurn"


class Forward(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        self.actuators.set_speeds(0.8, 0.8)
    
    def get_name(self):
        return "Forward"

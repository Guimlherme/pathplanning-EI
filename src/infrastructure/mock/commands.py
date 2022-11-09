from command import Command

class Stopped(Command):
    def execute(self):
        return
    
    def get_name(self):
        return "Stopped"

class HalfTurn(Command):
    def execute(self):
        print("HalfTurn")

    def get_name(self):
        return "HalfTurn"

class Forward(Command):
    def __init__(self, angle):
        self.line_angle = angle

    def execute(self):
        pass
    
    def get_name(self):
        return "Forward"

class MockCommandFactory:
    def stopped(self):
        return Stopped()

    def forward(self, line_angle):
        return Forward(line_angle)

    def half_turn(self):
        return HalfTurn()

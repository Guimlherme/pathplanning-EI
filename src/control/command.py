class Command:
    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def execute(self):
        print("Stopped")

class HalfTurn(Command):
    def execute(self):
        print("HalfTurn")

class Forward(Command):
    def __init__(angle):
        self.line_angle = angle

    def execute(self):
        print("Forward")
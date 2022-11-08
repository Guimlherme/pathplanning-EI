class Command:
    def get_name(self):
        return "Abstract Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def execute(self):
        print("Stopped")
    
    def get_name(self):
        return "Stopped"

class HalfTurn(Command):
    def execute(self):
        print("HalfTurn")

    def get_name(self):
        return "HalfTurn"

class Forward(Command):
    def __init__(angle):
        self.line_angle = angle

    def execute(self):
        print("Forward")
    
    def get_name(self):
        return "Forward"
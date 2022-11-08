from .robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from .robust_serial.utils import open_serial_port
from time import sleep

motor_speed=50

class Command:
    def __init__(self, arduino):
        self.arduino = arduino

    def get_name(self):
        return "Abstract Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def __init__(self, arduino):
        super().__init__(arduino)

    def execute(self):
        return
    
    def get_name(self):
        return "Stopped"

class HalfTurn(Command):
    def __init__(self, arduino):
        super().__init__(arduino)
        
    def execute(self):
        print("HalfTurn")

    def get_name(self):
        return "HalfTurn"

class Forward(Command):
    def __init__(self, arduino, angle):
        self.line_angle = angle
        super().__init__(arduino)

    def execute(self):
        print("Moving forward at " + str(self.arduino.motor_speed) + "%...")
        write_order(self.arduino.serial_file, Order.MOTOR)
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur droit
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur gauche
        return
    
    def get_name(self):
        return "Forward"

class ArduinoCommandFactory:
    def __init__(self, arduino):
        self.arduino = arduino

    def stopped(self):
        return Stopped(self.arduino)

    def forward(self, line_angle):
        return Forward(self.arduino, line_angle)

    def halfturn(self):
        return HalfTurn(self.arduino)

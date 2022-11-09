from .robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from time import sleep
from command import Command

motor_speed=50

class ArduinoCommandFactory:
    def __init__(self, arduino):
        self.arduino = arduino

    def stopped(self):
        return Stopped(self.arduino)

    def forward(self, line_angle):
        return Forward(self.arduino, line_angle)

    def halfturn(self):
        return HalfTurn(self.arduino)

class ArduinoCommand(Command):
    def __init__(self, arduino):
        self.arduino = arduino

    def get_name(self):
        return "Abstract Arduino Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(ArduinoCommand):
    def __init__(self, arduino):
        super().__init__(arduino)

    def execute(self):
        write_order(serial_file, Order.STOP)
    
    def get_name(self):
        return "Stopped"

class HalfTurn(ArduinoCommand):
    def __init__(self, arduino):
        super().__init__(arduino)
        
    def execute(self):
        print("HalfTurn")
        # TODO: currently it is stopping, change to half turn
        write_order(serial_file, Order.STOP)

    def get_name(self):
        return "HalfTurn"

class Forward(ArduinoCommand):
    def __init__(self, arduino, angle):
        self.line_angle = angle
        super().__init__(arduino)

    def execute(self):
        print("Moving forward at " + str(self.arduino.motor_speed) + "%...")
        write_order(self.arduino.serial_file, Order.MOTOR)
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur droit
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur gauche
    
    def get_name(self):
        return "Forward"

